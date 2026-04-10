#!/usr/bin/env python3
"""
Joulegram JAP Receipt — Signing Reference Implementation
Whitepaper §6-8 — github.com/joulesgram/protocol

This module defines the canonical JSON serialization rules and Ed25519
signing/verification logic for JAP receipts. The app-side TypeScript
signing code in joulesgram/app MUST produce byte-identical canonical
JSON to this module, otherwise signatures will not verify.

Canonicalization rules (must match across all JAP implementations):

    1. Sort object keys lexicographically (Python's sort_keys=True)
    2. No whitespace between tokens (separators=(',', ':'))
    3. ASCII-only encoding with \\uXXXX escapes for non-ASCII (ensure_ascii=True)
    4. No trailing newline
    5. UTF-8 byte encoding of the resulting string

The operator signature covers the receipt body with all fields EXCEPT
the `operator_sig` field itself. Do not include the signature field
when computing the signing basis.

Usage:

    from sign_receipt import sign_receipt, verify_receipt, load_private_key

    key = load_private_key("~/.joulegram/operator_ed25519.pem")

    receipt = {
        "receipt_version": "jap_v0.1",
        "request_id": "req_abc123",
        # ... all other required fields ...
        # (do NOT include operator_sig here)
    }

    receipt["operator_sig"] = sign_receipt(receipt, key)
    # receipt is now a complete signed JAP receipt

    # Verification:
    public_key = key.public_key()
    assert verify_receipt(receipt, public_key)
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.exceptions import InvalidSignature


# Fields that must be present in a JAP v0.1 receipt.
REQUIRED_RECEIPT_FIELDS: frozenset[str] = frozenset(
    {
        "receipt_version",
        "request_id",
        "model_id",
        "model_version",
        "input_hash",
        "output_hash",
        "tokens_in",
        "tokens_out",
        "energy_kj",
        "energy_attestation",
        "timestamp",
        "merkle_epoch",
    }
)

# Valid energy attestation levels per Whitepaper §10.
VALID_ATTESTATION_LEVELS: frozenset[str] = frozenset({"L0", "L1", "L2", "L3", "L4"})


def canonical_json(obj: Any) -> bytes:
    """
    Serialize a JSON-compatible Python object to canonical JSON bytes.

    The canonicalization is deterministic: same input always produces
    the same output bytes, across Python versions and platforms.

    Rules (must match the TypeScript app-side implementation exactly):
      - Sort keys lexicographically
      - No whitespace (separators=(',', ':'))
      - ASCII-only with \\uXXXX escapes for non-ASCII
      - UTF-8 encoding
      - No trailing newline

    Returns:
        UTF-8 encoded canonical JSON bytes.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def compute_signing_basis(receipt: dict[str, Any]) -> bytes:
    """
    Compute the canonical bytes that should be signed for this receipt.

    The signing basis is the receipt object with the `operator_sig` field
    removed (if present), canonicalized to JSON bytes.

    This function does NOT mutate the input receipt.
    """
    receipt_for_signing = {k: v for k, v in receipt.items() if k != "operator_sig"}
    return canonical_json(receipt_for_signing)


def validate_receipt_shape(receipt: dict[str, Any]) -> None:
    """
    Validate that a receipt has the required fields for JAP v0.1.

    This is a pre-signing shape check, not a full JSON Schema validation.
    For full validation, use the schema in schema/jap-receipt.schema.json
    with a JSON Schema library.

    Raises:
        ValueError: if the receipt is missing required fields or has
                    an invalid receipt_version or energy_attestation.
    """
    missing = REQUIRED_RECEIPT_FIELDS - set(receipt.keys())
    if missing:
        raise ValueError(
            f"Receipt missing required fields: {sorted(missing)}"
        )

    if receipt["receipt_version"] != "jap_v0.1":
        raise ValueError(
            f"Unsupported receipt_version: {receipt['receipt_version']!r} "
            f"(expected 'jap_v0.1')"
        )

    if receipt["energy_attestation"] not in VALID_ATTESTATION_LEVELS:
        raise ValueError(
            f"Invalid energy_attestation: {receipt['energy_attestation']!r} "
            f"(expected one of {sorted(VALID_ATTESTATION_LEVELS)})"
        )


def sign_receipt(
    receipt: dict[str, Any],
    private_key: Ed25519PrivateKey,
) -> str:
    """
    Sign a JAP receipt with the operator's Ed25519 private key.

    The receipt should NOT contain an `operator_sig` field when passed
    to this function (if it does, the existing value is ignored and
    replaced). Returns the base64-encoded signature, which the caller
    should set as receipt["operator_sig"].

    Args:
        receipt: The receipt dict without operator_sig. All other required
                 fields must be present.
        private_key: The operator's Ed25519 private key.

    Returns:
        Base64-encoded Ed25519 signature (no padding).

    Raises:
        ValueError: if the receipt shape is invalid.
    """
    # Shape check (without operator_sig since we haven't added it yet)
    shape_check = {k: v for k, v in receipt.items() if k != "operator_sig"}
    validate_receipt_shape(shape_check)

    basis = compute_signing_basis(receipt)
    signature_bytes = private_key.sign(basis)
    return base64.b64encode(signature_bytes).decode("ascii").rstrip("=")


def verify_receipt(
    receipt: dict[str, Any],
    public_key: Ed25519PublicKey,
) -> bool:
    """
    Verify the operator signature on a JAP receipt.

    Args:
        receipt: A complete signed receipt including operator_sig.
        public_key: The operator's Ed25519 public key.

    Returns:
        True if the signature is valid, False otherwise.
    """
    if "operator_sig" not in receipt:
        return False

    try:
        validate_receipt_shape(receipt)
    except ValueError:
        return False

    sig_b64 = receipt["operator_sig"]
    # Restore base64 padding if it was stripped
    padding = "=" * (-len(sig_b64) % 4)
    try:
        signature_bytes = base64.b64decode(sig_b64 + padding)
    except Exception:
        return False

    basis = compute_signing_basis(receipt)

    try:
        public_key.verify(signature_bytes, basis)
        return True
    except InvalidSignature:
        return False


def hash_receipt(receipt: dict[str, Any]) -> str:
    """
    Compute the canonical SHA-256 hash of a complete signed receipt.

    This is the hash used as a leaf in the daily Merkle tree. The full
    receipt (including operator_sig) is hashed, not just the signing basis.

    Returns:
        SHA-256 digest in "sha256:<64 hex chars>" format.
    """
    digest = hashlib.sha256(canonical_json(receipt)).hexdigest()
    return f"sha256:{digest}"


def load_private_key(path: str | Path) -> Ed25519PrivateKey:
    """
    Load an Ed25519 private key from a PEM file.

    Raises:
        ValueError: if the key is not Ed25519.
        FileNotFoundError: if the file does not exist.
    """
    path = Path(path).expanduser()
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError(
            f"Key at {path} is not an Ed25519 private key "
            f"(got {type(key).__name__})"
        )
    return key


def load_public_key(path: str | Path) -> Ed25519PublicKey:
    """
    Load an Ed25519 public key from a PEM file.

    Raises:
        ValueError: if the key is not Ed25519.
        FileNotFoundError: if the file does not exist.
    """
    path = Path(path).expanduser()
    with open(path, "rb") as f:
        key = serialization.load_pem_public_key(f.read())
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError(
            f"Key at {path} is not an Ed25519 public key "
            f"(got {type(key).__name__})"
        )
    return key


def public_key_fingerprint(key: Ed25519PrivateKey | Ed25519PublicKey) -> str:
    """
    Compute a short identifier for an Ed25519 public key.

    The fingerprint is SHA-256 of the DER-encoded SubjectPublicKeyInfo,
    base64-encoded, with the sha256: prefix. Used in daily Merkle root
    files to identify which key signed the root.
    """
    if isinstance(key, Ed25519PrivateKey):
        pub = key.public_key()
    else:
        pub = key
    der = pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    digest = hashlib.sha256(der).digest()
    return "sha256:" + base64.b64encode(digest).decode("ascii").rstrip("=")


# ─── Self-test ─────────────────────────────────────────────────────────────────

def _self_test() -> None:
    """Round-trip sign/verify test. Run with: python sign_receipt.py"""
    print("Generating test Ed25519 keypair...")
    key = Ed25519PrivateKey.generate()
    pub = key.public_key()
    print(f"Fingerprint: {public_key_fingerprint(key)}")

    receipt = {
        "receipt_version": "jap_v0.1",
        "request_id": "req_selftest_001",
        "model_id": "claude-sonnet-4-20250514",
        "model_version": "2026.03.14",
        "input_hash": "sha256:" + "a" * 64,
        "output_hash": "sha256:" + "b" * 64,
        "tokens_in": 1247,
        "tokens_out": 389,
        "energy_kj": 40.9,
        "energy_attestation": "L0",
        "timestamp": "2026-04-08T14:23:11.142Z",
        "provider_sig": None,
        "merkle_epoch": "2026-04-08",
    }

    print("\nSigning receipt...")
    receipt["operator_sig"] = sign_receipt(receipt, key)
    print(f"Signature: {receipt['operator_sig']}")

    print("\nVerifying...")
    assert verify_receipt(receipt, pub), "Signature verification failed"
    print("✓ Signature verified")

    print("\nComputing leaf hash...")
    leaf = hash_receipt(receipt)
    print(f"Leaf hash: {leaf}")

    print("\nTampering with receipt (changing tokens_in)...")
    tampered = dict(receipt)
    tampered["tokens_in"] = 9999
    assert not verify_receipt(tampered, pub), "Tampered receipt should not verify"
    print("✓ Tampered receipt correctly rejected")

    print("\nAll self-tests passed.")


if __name__ == "__main__":
    _self_test()
