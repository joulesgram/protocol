#!/usr/bin/env python3
"""
Joulegram JAP Receipt — Daily Merkle Root Publisher
Whitepaper §8 — github.com/joulesgram/protocol/blob/main/WHITEPAPER.md

Reads all JAP receipts for a given UTC date from the protocol database,
validates them, builds a Merkle tree over their canonical hashes, signs
the entire output with the operator Ed25519 key, and writes the canonical
daily root file to merkle-roots/YYYY-MM-DD.json.

Every day this script succeeds is a day on the 90-day reliability clock
that the legal-AI pilot pitch depends on. Every day it fails resets that
clock. Protect this script accordingly.

Usage:
    python daily_merkle.py                         # publish yesterday UTC
    python daily_merkle.py --date 2026-04-09       # publish a specific date
    python daily_merkle.py --from-json test.json   # test mode, reads from file
    python daily_merkle.py --dry-run               # compute without writing
    python daily_merkle.py --verify 2026-04-08     # verify an existing root file

Environment variables:
    DATABASE_URL          Postgres connection string. Required unless --from-json.
    OPERATOR_KEY_PATH     Path to Ed25519 private key PEM.
                          Default: ~/.joulegram/operator_ed25519.pem
    PROTOCOL_REPO_PATH    Path to the joulesgram/protocol repo clone.
                          Default: ./protocol

Exit codes:
    0   Success
    1   Transient failure (retry)
    2   Configuration error (fix and retry)
    3   Integrity failure (do not retry automatically — investigate)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any

# Import the shared canonicalization + signing logic.
# This ensures daily_merkle.py and the app-side signing always agree.
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sign_receipt import (  # noqa: E402
    canonical_json,
    hash_receipt,
    load_private_key,
    public_key_fingerprint,
    validate_receipt_shape,
    verify_receipt,
    load_public_key,
)

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    import base64
    import hashlib
except ImportError:
    print("ERROR: cryptography library not installed.", file=sys.stderr)
    print("Run: pip install cryptography", file=sys.stderr)
    sys.exit(2)


SCHEMA_VERSION = "merkle_v0.1"
UTC = dt.timezone.utc


# ─── Merkle tree construction ──────────────────────────────────────────────────


def build_merkle_tree(leaf_hashes: list[str]) -> str:
    """
    Build a Bitcoin-style Merkle tree over the leaf hashes and return the root.

    Rules:
      - Leaves are SHA-256 hashes in "sha256:<64 hex>" format
      - If a level has an odd number of nodes, the last node is duplicated
      - Parents are sha256(left_bytes || right_bytes) where *_bytes are the
        raw 32-byte digests (not the hex strings)

    Returns:
        Merkle root in "sha256:<64 hex>" format. For an empty leaf list,
        returns sha256:<hash of empty string> as the canonical empty-tree root.
    """
    if not leaf_hashes:
        empty_digest = hashlib.sha256(b"").hexdigest()
        return f"sha256:{empty_digest}"

    current = list(leaf_hashes)

    while len(current) > 1:
        if len(current) % 2 == 1:
            current.append(current[-1])

        next_level: list[str] = []
        for i in range(0, len(current), 2):
            left_hex = current[i].removeprefix("sha256:")
            right_hex = current[i + 1].removeprefix("sha256:")
            combined = bytes.fromhex(left_hex) + bytes.fromhex(right_hex)
            parent = hashlib.sha256(combined).hexdigest()
            next_level.append(f"sha256:{parent}")

        current = next_level

    return current[0]


# ─── Receipt loading ───────────────────────────────────────────────────────────


def load_receipts_from_db(db_url: str, target_date: dt.date) -> list[dict[str, Any]]:
    """
    Load receipts from the Postgres jap_receipts table for a given date.

    The table is expected to have at minimum:
        request_id TEXT
        merkle_epoch DATE
        receipt_json JSONB
    with an index on (merkle_epoch, request_id).
    """
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("ERROR: psycopg2-binary not installed.", file=sys.stderr)
        print("Run: pip install psycopg2-binary", file=sys.stderr)
        sys.exit(2)

    conn = psycopg2.connect(db_url)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT receipt_json
                FROM jap_receipts
                WHERE merkle_epoch = %s
                ORDER BY request_id ASC
                """,
                (target_date.isoformat(),),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [row["receipt_json"] for row in rows]


def load_receipts_from_json(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array of receipts, got {type(data).__name__}")
    return data


# ─── Previous root lookup ──────────────────────────────────────────────────────


def find_previous_root(
    roots_dir: Path,
    target_date: dt.date,
) -> str | None:
    """
    Find the most recent Merkle root file before target_date and return its
    merkle_root value. Used to chain-link the new file to the prior one.

    Returns None if no prior file exists (genesis case).
    """
    if not roots_dir.exists():
        return None

    candidates: list[tuple[dt.date, Path]] = []
    for f in roots_dir.iterdir():
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            file_date = dt.date.fromisoformat(f.stem)
        except ValueError:
            continue
        if file_date < target_date:
            candidates.append((file_date, f))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    most_recent = candidates[0][1]

    with open(most_recent, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("merkle_root")


# ─── Output signing ────────────────────────────────────────────────────────────


def sign_output(
    output: dict[str, Any],
    private_key: Ed25519PrivateKey,
) -> str:
    """
    Sign the canonical form of the output object, excluding the signature field.

    The signature thus covers the epoch_date, merkle_root, receipt_count,
    previous_root, and all other output fields — not just the merkle_root.
    This prevents an attacker from swapping out metadata around a valid root.
    """
    to_sign = {k: v for k, v in output.items() if k != "signature"}
    basis = canonical_json(to_sign)
    signature_bytes = private_key.sign(basis)
    return base64.b64encode(signature_bytes).decode("ascii").rstrip("=")


def verify_output_signature(
    output: dict[str, Any],
    public_key: Ed25519PublicKey,
) -> bool:
    """Verify the signature on a daily root file."""
    if "signature" not in output:
        return False
    sig_b64 = output["signature"]
    padding = "=" * (-len(sig_b64) % 4)
    try:
        signature_bytes = base64.b64decode(sig_b64 + padding)
    except Exception:
        return False

    to_verify = {k: v for k, v in output.items() if k != "signature"}
    basis = canonical_json(to_verify)

    try:
        public_key.verify(signature_bytes, basis)
        return True
    except Exception:
        return False


# ─── Main publish flow ─────────────────────────────────────────────────────────


def publish(
    target_date: dt.date,
    receipts: list[dict[str, Any]],
    private_key: Ed25519PrivateKey,
    roots_dir: Path,
    dry_run: bool,
) -> dict[str, Any]:
    """
    Publish a daily Merkle root for the given date.

    Returns the output dict. If dry_run is False and receipts are not empty,
    also writes the output file to roots_dir.
    """
    # Validate every receipt's shape and merkle_epoch
    for i, receipt in enumerate(receipts, 1):
        try:
            validate_receipt_shape(receipt)
        except ValueError as e:
            raise SystemExit(
                f"INTEGRITY ERROR: receipt #{i} (request_id={receipt.get('request_id', '?')}) "
                f"failed shape validation: {e}"
            )

        if receipt.get("merkle_epoch") != target_date.isoformat():
            raise SystemExit(
                f"INTEGRITY ERROR: receipt #{i} (request_id={receipt.get('request_id', '?')}) "
                f"has merkle_epoch={receipt.get('merkle_epoch')} but target date is "
                f"{target_date.isoformat()}. Refusing to publish mismatched epoch."
            )

    # Sort for deterministic ordering
    receipts.sort(key=lambda r: r["request_id"])

    # Check for duplicate request_ids within the epoch
    seen_ids: set[str] = set()
    for r in receipts:
        rid = r["request_id"]
        if rid in seen_ids:
            raise SystemExit(
                f"INTEGRITY ERROR: duplicate request_id in epoch: {rid}. "
                f"Refusing to publish with ambiguous receipts."
            )
        seen_ids.add(rid)

    # Hash each receipt to form the Merkle leaves
    leaf_hashes = [hash_receipt(r) for r in receipts]

    # Build the Merkle tree
    merkle_root = build_merkle_tree(leaf_hashes)

    # Find the previous root (chain link)
    previous_root = find_previous_root(roots_dir, target_date)

    # Assemble the output (without signature first)
    output: dict[str, Any] = {
        "epoch_version": SCHEMA_VERSION,
        "epoch_date": target_date.isoformat(),
        "receipt_count": len(receipts),
        "merkle_root": merkle_root,
        "operator_pubkey_fingerprint": public_key_fingerprint(private_key),
        "first_receipt_id": receipts[0]["request_id"] if receipts else None,
        "last_receipt_id": receipts[-1]["request_id"] if receipts else None,
        "previous_root": previous_root,
        "generated_at": dt.datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

    # Sign everything above
    output["signature"] = sign_output(output, private_key)

    # Write to disk unless dry-running
    if not dry_run:
        roots_dir.mkdir(parents=True, exist_ok=True)
        out_path = roots_dir / f"{target_date.isoformat()}.json"

        if out_path.exists():
            raise SystemExit(
                f"ERROR: {out_path} already exists. Refusing to overwrite.\n"
                f"The Merkle root file chain is append-only. If you need to regenerate, "
                f"delete the existing file manually AND publish an incident report."
            )

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
            f.write("\n")

        print(f"✓ Wrote {out_path}")

    return output


# ─── Verify mode ───────────────────────────────────────────────────────────────


def verify_mode(date_str: str, protocol_repo: Path) -> int:
    """
    Verify an existing daily root file:
      - Signature matches the committed operator public key
      - Chain link to previous file is correct
      - File is well-formed
    """
    roots_dir = protocol_repo / "merkle-roots"
    target_file = roots_dir / f"{date_str}.json"
    if not target_file.exists():
        print(f"ERROR: {target_file} does not exist", file=sys.stderr)
        return 2

    print(f"Verifying {target_file}")

    with open(target_file, "r", encoding="utf-8") as f:
        output = json.load(f)

    # Load the committed public key
    pubkey_path = protocol_repo / "keys" / "operator_pubkey.pem"
    if not pubkey_path.exists():
        print(f"ERROR: operator public key not found at {pubkey_path}", file=sys.stderr)
        return 2

    public_key = load_public_key(pubkey_path)

    # Check signature
    if not verify_output_signature(output, public_key):
        print("✗ Signature verification FAILED", file=sys.stderr)
        return 3
    print("✓ Signature valid")

    # Check chain link
    target_date = dt.date.fromisoformat(date_str)
    expected_prev = find_previous_root(roots_dir, target_date)
    if output.get("previous_root") != expected_prev:
        print(
            f"✗ Chain link mismatch: file says previous_root={output.get('previous_root')}, "
            f"but filesystem says {expected_prev}",
            file=sys.stderr,
        )
        return 3
    print(f"✓ Chain link valid (previous_root={expected_prev})")

    print(f"✓ Daily root {date_str} verified")
    print(f"  receipts: {output.get('receipt_count')}")
    print(f"  root:     {output.get('merkle_root')}")
    return 0


# ─── Entry point ───────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Joulegram daily Merkle root publisher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="UTC date to publish (YYYY-MM-DD). Default: yesterday UTC.",
    )
    parser.add_argument(
        "--from-json",
        type=str,
        default=None,
        help="Read receipts from a JSON file instead of the database (for testing).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print the output without writing the root file.",
    )
    parser.add_argument(
        "--verify",
        type=str,
        default=None,
        metavar="YYYY-MM-DD",
        help="Verify an existing root file's signature and chain link. Exits without publishing.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Override the output directory. Default: $PROTOCOL_REPO_PATH/merkle-roots/",
    )
    args = parser.parse_args()

    protocol_repo = Path(os.environ.get("PROTOCOL_REPO_PATH", "./protocol")).expanduser()

    # Verify mode short-circuits
    if args.verify:
        return verify_mode(args.verify, protocol_repo)

    # Resolve target date
    if args.date:
        try:
            target_date = dt.date.fromisoformat(args.date)
        except ValueError:
            print(f"ERROR: --date must be YYYY-MM-DD, got: {args.date}", file=sys.stderr)
            return 2
    else:
        target_date = (dt.datetime.now(UTC) - dt.timedelta(days=1)).date()

    today_utc = dt.datetime.now(UTC).date()
    if target_date > today_utc:
        print(f"ERROR: cannot publish a root for a future date: {target_date}", file=sys.stderr)
        return 2

    print(f"Target date: {target_date.isoformat()} (UTC)")

    # Load receipts
    if args.from_json:
        try:
            receipts = load_receipts_from_json(Path(args.from_json).expanduser())
        except Exception as e:
            print(f"ERROR: failed to load receipts from {args.from_json}: {e}", file=sys.stderr)
            return 2
        print(f"Loaded {len(receipts)} receipts from {args.from_json}")
    else:
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            print("ERROR: DATABASE_URL env var not set. Use --from-json for testing.", file=sys.stderr)
            return 2
        try:
            receipts = load_receipts_from_db(db_url, target_date)
        except Exception as e:
            print(f"ERROR: database query failed: {e}", file=sys.stderr)
            return 1
        print(f"Loaded {len(receipts)} receipts from database")

    # Load operator private key
    key_path = Path(
        os.environ.get("OPERATOR_KEY_PATH", "~/.joulegram/operator_ed25519.pem")
    ).expanduser()
    if not key_path.exists():
        print(f"ERROR: operator key not found at {key_path}", file=sys.stderr)
        print("Generate one with:", file=sys.stderr)
        print("  mkdir -p ~/.joulegram", file=sys.stderr)
        print("  openssl genpkey -algorithm ed25519 -out ~/.joulegram/operator_ed25519.pem", file=sys.stderr)
        print(
            "  openssl pkey -in ~/.joulegram/operator_ed25519.pem -pubout "
            "-out protocol/keys/operator_pubkey.pem",
            file=sys.stderr,
        )
        return 2

    try:
        private_key = load_private_key(key_path)
    except Exception as e:
        print(f"ERROR: failed to load operator key: {e}", file=sys.stderr)
        return 2

    # Resolve output directory
    if args.output_dir:
        roots_dir = Path(args.output_dir).expanduser()
    else:
        roots_dir = protocol_repo / "merkle-roots"

    # Publish (or dry-run)
    try:
        output = publish(
            target_date=target_date,
            receipts=receipts,
            private_key=private_key,
            roots_dir=roots_dir,
            dry_run=args.dry_run,
        )
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            return 3
        raise

    print()
    print(json.dumps(output, indent=2))
    print()

    if args.dry_run:
        print("[dry-run] Skipping file write and git suggestion.")
        return 0

    if not args.from_json:
        print("Next steps:")
        print(f"  cd {protocol_repo}")
        print(f"  git add merkle-roots/{target_date.isoformat()}.json")
        print(
            f"  git commit -m 'Daily Merkle root: {target_date.isoformat()} "
            f"({len(receipts)} receipts)'"
        )
        print("  git push")

    return 0


if __name__ == "__main__":
    sys.exit(main())
