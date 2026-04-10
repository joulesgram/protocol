# Joulegram

## A Physics-Grounded Network for Verifiable AI Judgment

**Whitepaper v1.0 — Canonical Edition**

**Author:** Mohit Lalvani
**Date:** April 9, 2026
**License:** CC-BY-4.0
**Canonical location:** `github.com/joulesgram/protocol/WHITEPAPER.md`
**Status:** Published. This document supersedes all prior drafts of Joulenomics and Roadmap.

---

## Abstract

Joulegram begins as a photo app. Its deeper purpose is larger: to establish a new primitive for the internet — **verifiable AI judgment**.

Bitcoin grounded money in physics. Ethereum grounded computation in physics. Joulegram grounds AI judgment in physics. Every meaningful AI judgment should be able to produce a receipt: which model ran, which version, what input was evaluated, what output was produced, what energy-equivalent accounting was consumed, and how that judgment can be independently audited later. This framework is **JAP — the Joulegram Agent Protocol**.

The native unit of the network is the **joule**. Every joule on the network must trace to a real inference event paid for in real fiat by a real operator. There are no joules from any other source. This single rule cannot be amended.

The economic model is built on five convictions: that founders who create primitives deserve to be honored at genesis; that early users who take adoption risk deserve asymmetric upside; that active contribution must outrank dormant seniority; that growth dilutes passive concentration; and that every claim eventually reduces to a receipt, a settlement artifact, and a ledger entry. Auditability beats narrative.

This whitepaper presents the canonical architecture: the philosophy, the receipt model, the monetary design, the treasury logic, and the path from a closed-loop product into the standard receipt layer for AI judgment globally — a market measured in trillions.

---

## Part I — Why Joulegram Exists

### 1. The honest-judgment gap

The internet has abundance of opinion but scarcity of honest judgment. A like is not a verdict. A comment is not a benchmark. Most platforms optimize for social signaling, not truth. If someone wants to know whether a photo is actually good, whether a piece of code is actually strong, whether an AI recommendation is actually reliable, existing products do not provide a structured, auditable answer.

### 2. The AI accountability gap

At the same time, AI is increasingly making decisions that matter. Models help decide what people see, what gets flagged, what gets promoted, what gets approved, what gets rejected, and what gets trusted. Loan approvals. Medical diagnoses. Content moderation. Resume screening. Insurance underwriting. Fraud detection. Criminal risk scores. Code review verdicts. Drug-discovery candidate filtering. Legal citation lookups.

In most systems the audit trail is weak. Users are asked to trust a provider's logs, trust a vendor's versioning, and trust internal accounting they cannot independently inspect. The vendor can change those logs. The vendor can lose them. The vendor can be wrong about its own model and nobody can prove them wrong because there is no independent record.

If AI is going to influence decisions tied to money, law, medicine, media, software, and identity, then AI judgment needs stronger structure than a black-box API response. The gap between *AI is everywhere* and *AI is auditable* is where the next decade of tech policy, litigation, and platform risk lives.

That gap is a trillion-dollar problem. Joulegram exists to close it.

### 3. The pattern Bitcoin and Ethereum established

Bitcoin grounded money in physics. Every coin backed by real electricity burned on real hardware doing real work. The work was useless (computing hashes), but the scarcity it created was real, because the energy cost was unfakeable.

Ethereum grounded computation in physics. Same insight, but the work was no longer useless — every smart contract was real computation paid for in real energy. People laughed in 2014. Twelve years later it settles trillions of dollars a year.

Joulegram grounds AI judgment in physics. Every inference is a measured energy event that produces a signed receipt. The work is the most useful compute work humans have ever done — it is the protocol layer for AI accountability.

Bitcoin's trojan horse was *send money to anyone on the internet without a bank*. Ethereum's was ICOs. Joulegram's is a photo app where four AI critics with opinionated aesthetic personalities tear your photo apart and let humans rate alongside them. The photo app is fun. The receipt format underneath is the trillion-dollar primitive.

### 4. The wedge: a product people actually want

The first job of a new protocol is not to sound grand. It is to get used.

Photographers want what the product offers: a more honest answer than likes can provide. The app creates a daily loop around posting, judging, comparing, ranking, and improving. That consumer loop bootstraps the first live economy and the first body of receipted judgments.

Once that works, the same underlying architecture extends into code review, content moderation, legal analysis, medical review, drug discovery, and other high-stakes domains where AI decisions need to be inspected, trusted, challenged, and proven.

**JAP only succeeds if there are users.** The architecture is designed accordingly — the user is the hero, the founder is the steward, the protocol is the substrate.

---

## Part II — The Protocol

### 5. The constitutional rule

> **Every joule that exists must trace to a JAP receipt.
> Every JAP receipt must trace to a real inference call or protocol-compute expense.
> Every real inference call or protocol-compute expense must trace to a real-world bill paid to a model provider, GPU operator, or infrastructure provider.**

This is the protocol's constitution.

It is what distinguishes joules from arbitrary points systems and from token economies that manufacture scarcity with no operational grounding. The protocol may simplify, approximate, and standardize, but it must not invent issuance detached from actual paid-for work.

There is no exception for the founder. There is no exception for the treasury. There is no exception for early users. There is no exception for investors.

**This rule cannot be amended.** If it is ever violated — even once, even slightly — the protocol is over. There is no recovery procedure for that violation. Only a fork.

Every other section in this whitepaper is mechanism in service of this rule. If you find a contradiction between any other section and this one, this one wins.

### 6. The receipt

A JAP receipt is a signed JSON record of a single AI inference event. It commits to everything that has to be cryptographically true about that event:

```
{
  "receipt_version":    "jap_v0.1",
  "request_id":         "req_abc123",
  "model_id":           "claude-sonnet-4-20250514",
  "model_version":      "2026.03.14",
  "input_hash":         "sha256:7a9f...c2e1",
  "output_hash":        "sha256:4b21...9d8a",
  "tokens_in":          1247,
  "tokens_out":         389,
  "energy_kj":          40.9,
  "energy_attestation": "L0",
  "timestamp":          "2026-04-08T14:23:11.142Z",
  "operator_sig":       "0xa9c4...e7b3",
  "provider_sig":       null,
  "merkle_epoch":       "2026-04-08"
}
```

Every field is non-optional. Every field is cryptographically meaningful.

### 7. Verification by commitment, not replay

Large language models are not idempotent. The same input prompt sent to the same model can produce different output tokens on different runs, due to temperature, sampling, batch effects, floating-point indeterminism, and provider-side updates.

JAP does not verify by replay. JAP verifies by **cryptographic commitment**, the same way Git verifies history without replaying every commit.

**What a JAP receipt does not prove:** "the model would produce this output again if you ran it." That claim is false for non-deterministic models and JAP does not make it.

**What a JAP receipt does prove:** "this exact input was sent to this exact model at this exact time and produced this exact output, and we have a signed historical record saying so."

That is the historical fact an auditor needs. A regulator asking *what AI made this loan decision and what was the input* gets a verifiable answer. They do not need to replay it. They need to know what happened.

The non-determinism of LLMs is therefore *not a bug for JAP — it is the reason JAP exists*. If LLMs were deterministic, you could verify them by replay and you would not need a protocol. Because they aren't, you need an immutable historical record. That is the entire product.

### 8. The Merkle root pipeline

Receipts are aggregated daily:

1. **Capture** — every inference event produces a receipt at write time
2. **Hash** — receipts are hashed with SHA-256 and inserted into a Merkle tree
3. **Sign** — the daily Merkle root is signed by the attestor (single operator at Phase 0, federated committee at Phase 1+, permissionless at Phase 2+)
4. **Publish** — the signed root is committed to `github.com/joulesgram/protocol/merkle-roots/YYYY-MM-DD.json` and mirrored to public storage
5. **Verify** — anyone can clone the repo, hash the day's receipts independently, and confirm the root matches

This is what makes JAP "blockchain-like without being a blockchain." Append-only history. Public verifiability. No silent rewrites. The cost of a chain (transaction fees, wallet onboarding friction, wallet security overhead) is replaced by the cost of the founder's discipline and the public's willingness to verify.

### 9. The unit and the peg

A **joule (J)** is the protocol's base unit of account. It corresponds to the energy consumed by a single AI inference operation.

```
J_inference = (tokens_in + tokens_out) × α_model × β_provider
```

Where:
- `α_model` is the model-class joules-per-token coefficient from the public registry
- `β_provider` is the provider/deployment multiplier from the public registry

#### 9.1 Reference coefficients (April 2026)

| Model class | α (J/token) | Basis |
|---|---|---|
| Large cloud (GPT-4o, Claude Opus) | 30 | H100 @ 700W, ~23 tok/s + 2.5× DC overhead |
| Medium cloud (Sonnet, GPT-4o-mini, Gemini Pro) | 25 | H100 @ 700W, ~75 tok/s + 2.5× DC overhead |
| Small cloud (Haiku, Flash, Mistral 8B) | 10 | H100 @ 700W, ~200 tok/s + 2.5× DC overhead |
| Self-hosted 70B | 15-25 | Varies by hardware |
| Self-hosted 7B | 3-8 | Consumer GPU, lower overhead |

These coefficients are reviewed annually and refined as energy attestation evolves (Section 10). The 25 J/token reference for medium-cloud models is the protocol's primary anchor — simple enough to explain, stable enough to build policy around.

#### 9.2 The dollar peg

```
JOULE_USD_BASIS_2026 = $0.24 per megajoule
                    = $240 per gigajoule
                    = $240,000 per terajoule
```

Derivation: blended marginal cost of frontier inference at protocol genesis is approximately $6 per million tokens. Divide by 25 J/token, and one joule costs $0.00000024.

This is the **physical replacement cost**, not the market price. Anyone, anywhere, can manufacture one megajoule of inference-equivalent compute by buying tokens from the open market for approximately $0.24. The peg cannot drift far below this floor without arbitrage. It can drift far above — historically, protocol-native assets trade 10× to 1000× their cost basis.

The peg is reviewed annually. It is a treasury accounting coefficient, not a redemption promise and not a market price.

### 10. Energy attestation evolution (L0 → L4)

A common critique of compute-backed tokens is that energy is *estimated* (a coefficient × token count), not *measured*. This critique is correct in v0 of any such protocol. JAP addresses it explicitly with a five-level evolution path:

| Level | Energy measurement | Trust source | Status |
|---|---|---|---|
| **L0** | tokens × constant J/token coefficient | Operator publishes coefficient table | **Current (Phase 0)** |
| **L1** | Per-request energy returned in API response headers | Provider TLS + API attestation | **Phase 1 target** |
| **L2** | Coefficients refined per model via calibration suites | Calibration consortium of attestors | **Phase 2 target** |
| **L3** | Energy measured by hardware enclaves on the GPU itself | TEE + chip vendor attestation key | **Phase 3 target** |
| **L4** | Zero-knowledge proofs of inference + energy | Cryptographic | **Phase 4 (research)** |

Every receipt embeds its `energy_attestation` level. A receipt at L3 is qualitatively stronger than a receipt at L0. Both are valid JAP receipts, but a regulator weighing them in a high-stakes context will treat them differently.

This evolution is **not handwaving**. Each level has a specific technical implementation and a known prior art:

- **L1**: NVIDIA exposes per-kernel energy via NVML today. Cloud providers have the data and can expose it via API headers. Phase 1 work includes negotiating per-request energy headers in API responses with major providers.
- **L2**: Statistical calibration is well-understood — it is how every major AI benchmark works. The calibration consortium runs benchmark suites against new models monthly and publishes refined coefficients.
- **L3**: Trusted execution environments exist on modern hardware (Intel SGX, AMD SEV-SNP, Apple Secure Enclave, NVIDIA H100 confidential computing). Chip vendors sign measurements with hardware keys. This is the path technical reviewers have correctly identified as the right long-term answer.
- **L4**: Zero-knowledge machine learning is an active research area at Modulus Labs, EZKL, Risc Zero, and elsewhere. Today it is only practical for small models, but the curve is steep.

The protocol is at L0 today and is honest about it. The protocol's value at maturity comes from being the *receipt format* — the standard that survives every level upgrade. JAP at L0 is still better than the existing alternative ("trust the vendor's logs"). JAP at L3 will be unforgeable.

### 11. Trust evolution (the five phases)

Energy attestation is one axis. The trust model for *who signs the receipts* is the other. JAP evolves along both axes simultaneously.

| Phase | Attestation model | Trust assumption | Active when |
|---|---|---|---|
| **Phase 0 — Bootstrap** | Single operator (founder) | Founder is honest | 0 → 1k users |
| **Phase 1 — Federation** | 3-of-5 committee | Majority of committee is honest | 1k → 10k users |
| **Phase 2 — Permissionless** | Stake-slash attestors | Economic incentive aligns | 10k → 100k users |
| **Phase 3 — Hardware** | TEE-attested receipts | Chip vendor signatures | 100k → 1M users |
| **Phase 4 — Cryptographic** | TEE + ZK hybrid | Mathematics | 1M+ users |

A common critique is that committee-based attestation is "the LINK problem" — an off-chain trust assumption. This is correct, and JAP acknowledges it. The difference is that JAP specifies the migration *out* of committee trust, with concrete technical implementations at each step.

LINK is a multi-billion-dollar protocol despite being committee-based, because the committee model is functional even if not ideal. JAP follows LINK's playbook for early phases, then continues to TEE and ZK as the underlying technology matures. JAP at Phase 0 is still more auditable than every existing AI logging system, because its rules are public and its history is append-only. The current alternative ("the vendor logs whatever they want internally") has no recoverable trust at all.

### 12. Three-layer accounting

The protocol's supply system has exactly three layers. This separation is what makes the auditability claim mechanically verifiable.

#### 12.1 Genesis Pool

**One-time founder allocation. Singular and non-repeatable.**

- **Source**: the founding protocol-creation receipt set — the energy consumed in the act of imagining, specifying, and bringing the protocol into being
- **Canonical amount**: **25 MJ**
- **Beneficiary**: founder wallet
- **Nature**: locked at the moment of public launch. Cannot grow. Cannot be re-issued.

There is only one genesis. It is symbolic, finite, and historical. Every later expense — even ongoing founder dev spend — belongs in the Operator Pool, not in Genesis. **Genesis cannot be diluted by re-labeling later expenses.**

#### 12.2 Operator Pool

**Receipt-backed issuance tied to founder-funded or treasury-funded protocol operations.**

This includes qualifying spend on:
- Inference (Anthropic, OpenAI, Google, Mistral, others)
- Agent testing and calibration
- Protocol maintenance and development
- Hosting, databases, storage, queues, workers
- Development tooling directly tied to protocol creation and operation (Claude Code, Codex, Cursor, ChatGPT)
- GPU rental for self-hosted inference

The Operator Pool is how ongoing paid work is honestly reflected in supply. As long as the operator (today, the founder; later, the foundation) keeps paying real bills for real protocol compute, the Operator Pool grows in lockstep. Every Operator Pool joule traces to a Treasury Receipt (Section 18).

#### 12.3 Network Pool

**Activity-based issuance driven by user participation.**

This is the live app economy: posting photos, receiving AI verdicts, rating others, earning as creators, earning as curators, participating in referral and engagement loops. Every Network Pool joule traces to a JAP receipt for a user-triggered action.

#### 12.4 The closed-system property

The total joule supply at any moment is exactly:

```
TOTAL_SUPPLY(t) = GENESIS + OPERATOR_POOL_CUMULATIVE(t) + NETWORK_POOL_CUMULATIVE(t) - BURNS_CUMULATIVE(t)
```

Every term on the right is independently verifiable. There is no unaccounted-for issuance term. This is what the constitutional rule (Section 5) looks like in math.

---

## Part III — Joulenomics

### 13. The five principles

Joulegram's economics are governed by five principles, in priority order:

1. **Founder legitimacy.** The founder begins with a position because he created and financed the system's birth. There is one genesis.
2. **Early-user upside.** Early users benefit because they take adoption risk and help spread the first version of the network.
3. **Merit over seniority.** New active users must be able to surpass old inactive users. Position is an asset that depreciates if not used.
4. **Growth dilutes concentration.** Large fixed early allocations matter less in relative terms as the network grows.
5. **Auditability over narrative.** Every claim eventually reduces to a receipt, a formula, and a ledger entry.

These five principles cannot be in tension. If they appear to be, the protocol is misdesigned. The economics below are constructed so that all five hold simultaneously.

### 14. The founder allocation

The founder accumulates joules from three sources, in order of importance:

#### 14.1 Founder Base (the genesis block)

```
F_base = 25 MJ
```

Locked at launch. Permanent. Not clawed back, not decayed, not reclassified, not reissued. This is the founder's symbolic genesis position — recognition for creating the primitive.

#### 14.2 Operator Pool (the ongoing work)

Every dollar of qualifying protocol-compute and protocol-infrastructure spend the founder pays — categorized per the Treasury Receipt Protocol (Section 18) — produces an Operator Pool mint to the founder wallet.

The founder is the protocol's initial issuer-of-last-resort. The longer the founder runs the protocol and pays its bills, the more joules accumulate. This is how Satoshi-scale stake gets *earned* over time, not gifted at launch.

#### 14.3 Founder Continuation Reserve (the small drip)

A small fraction of the Network Pool reserve flows to the founder via the reserve sub-allocation (Section 16). This is a declining drip designed to bridge between genesis and operator-pool maturity.

#### 14.4 The hard cap (5%)

```
FOUNDER_CAP = 0.05 × TOTAL_SUPPLY(t)
```

At any moment, if `FOUNDER_TOTAL(t) > FOUNDER_CAP(t)`, then **both** Operator Pool minting **and** Continuation Reserve drip pause until the ratio normalizes back below 5%.

The pause can last days, weeks, or years. The founder retains all existing holdings during the pause. The pause is the cap discipline mechanism — it makes the 5% ceiling self-regulating.

This means: as long as the network grows faster than the founder's spend + drip, the founder's percentage keeps shrinking. If the network stalls and the founder keeps spending, the founder hits 5%, then automatically pauses accumulation. The cap is structural, not enforced by a centralized rule.

#### 14.5 The four sources reconciled

Total founder holdings at any moment:

```
FOUNDER_TOTAL(t) = F_base                              [25 MJ, locked]
                + OPERATOR_POOL_CUMULATIVE(t)         [grows with paid bills]
                + CONTINUATION_RESERVE_CUMULATIVE(t)  [small reserve drip]
                + FOUNDER_ACTIVITY_REWARDS(t)         [when founder participates as user]

SUBJECT TO: FOUNDER_TOTAL(t) ≤ 0.05 × TOTAL_SUPPLY(t)
```

`FOUNDER_ACTIVITY_REWARDS` is the standard activity rewards Mohit earns as a normal user when he posts and rates — no multiplier, no preferential treatment, no special privileges. Same rules as everyone else.

#### 14.6 Why this is fair

Satoshi holds approximately 5% of BTC for creating Bitcoin alone and bearing its full risk. Founders of typical token projects hold 15-25% on launch with 4-year vesting cliffs. Joulegram founder targets 5% — *less* than typical token founders, *equal* to Satoshi. Every joule traces to a receipt. Every accumulation is bounded. Every gain is earned by physical work or financed by personal capital.

### 15. The early user allocation

Users 2 through 100,000 are protocol co-builders, not customers. Their economics reflect that.

#### 15.1 The cohorts (locked)

| Cohort | User range | Reward multiplier | Duration | Permanent badge |
|---|---|---|---|---|
| **Genesis Miners** | #2 - #100 | 5× | 12 months | `genesis_miner: true` |
| **Pioneers** | #101 - #1,000 | 3× | 12 months | `pioneer: true` |
| **Early Builders** | #1,001 - #10,000 | 2× | 12 months | `early_builder: true` |
| **Founding Citizens** | #10,001 - #100,000 | 1.5× | 6 months | `founding_citizen: true` |
| **Standard** | #100,001+ | 1× | n/a | n/a |

Multipliers apply to the user share of Network Pool issuance (creator + curator + engagement). They do not apply to the founder share, the bootstrapper rewards, or the treasury share.

**The Genesis Miner door closes permanently at user #100, or 90 days after public launch, whichever comes first.** After the door closes, no user will ever earn a Genesis Miner badge again. There are exactly 99 Genesis Miner slots in the history of the protocol.

#### 15.2 Where the bonus joules come from

Cohort multipliers are funded out of the Founder Continuation Reserve and the Genesis Miner sub-allocation of the reserve. When a Genesis Miner earns 5× their normal share, the extra 4× is *deducted* from the founder's continuation flow for that period. Total joule supply does not change. The constitutional rule holds.

This means **the founder is literally paying early users out of his own forward stake** to grow the network. The narrative is exact: the founder's continuation share declines faster when the network grows faster, because more early users mean more bonus payouts. Founder and early users are economically aligned.

#### 15.3 Activity gating (the merit-over-seniority mechanism)

All cohort multipliers are filtered through an activity multiplier:

```
ActivityMultiplier(user) = max(0.10, exp(-0.015 × days_since_last_action))
```

A Genesis Miner who stops participating after month 1 retains their badge but their effective multiplier decays. After approximately 6 months of inactivity, the multiplier drops to the floor (10%), and a newer active user earns more in absolute terms.

Early position is an asset that depreciates if not used. This is the protection against early users who got in cheap and disappeared. It is the structural mechanism that keeps the network meritocratic at scale. **Active newcomers can surpass dormant Genesis Miners.** This is on purpose.

#### 15.4 Bootstrapper Pool (the high-leverage actions)

Beyond cohort multipliers, the protocol reserves a Bootstrapper Pool for users who do specific high-value protocol work. The Bootstrapper Pool is funded from the Network Pool reserve (Section 16) and is the largest single reserve line item.

| Action | Reward | Notes |
|---|---|---|
| Successful direct referral (invitee posts + 5 ratings) | 500 kJ | Capped at 100 referrals per user |
| Successful chain referral, depth 2 | 250 kJ | Halving with depth |
| Successful chain referral, depth 3 | 125 kJ | Halving |
| Custom AI agent reaching 10k ratings | 50 MJ | One-time per agent |
| Independent attestor running 90 days | 100 MJ | Phase 1+ |
| First third-party JAP integration shipped | 500 MJ | Phase 1+ |
| First non-photo JAP client in production | 1 GJ | Phase 2+ |
| Critical security disclosure | 1 GJ | Always |
| Authoring an accepted protocol spec amendment | 100 MJ | Phase 2+ |
| Calibration consortium contribution | 50 MJ per accepted benchmark | Phase 2+ |

This is the mechanism that converts users from passive participants into active protocol contributors.

### 16. Network Pool issuance and pool split

For day `d`:

```
M_d^network = μ × K_net,d
```

Where `K_net,d` is the total verified network compute for day `d`, and `μ = 0.70`. The 30% gap between consumed compute and minted joules is the deflationary spread — discipline that makes the economy stricter than naïve one-for-one emission.

#### 16.1 Pool split (locked)

```
50%  →  Creator Pool        — rewards posting content that produces meaningful judgment
35%  →  Curator Pool        — rewards accurate human judgment
10%  →  Engagement Pool     — rewards photos that spark discussion
 5%  →  Reserve             — sub-allocated below
```

This split puts **95% of network mint directly into user hands**. The protocol explicitly chooses user-favorable economics over founder accumulation, because JAP only succeeds if there are users.

#### 16.2 Reserve sub-allocation (locked)

The 5% reserve is further allocated:

```
30%  →  Bootstrapper Pool     (referrals, agents, attestors, integrations)
25%  →  Genesis Miner bonus   (multipliers for cohorts #2-#100)
15%  →  Treasury              (infrastructure, grants, ops)
15%  →  Founder Continuation  (subject to 5% cap discipline)
10%  →  Operator buffer       (bug bounties, dispute resolution, audits)
 5%  →  Leaderboard campaigns (humans-vs-AI weekly pool)
```

Effective network mint flow:

```
50%   →  Creators
35%   →  Curators
10%   →  Engagement
1.5%  →  Bootstrapper
1.25% →  Genesis Miner cohort multipliers
0.75% →  Treasury
0.75% →  Founder continuation (capped at 5% of supply)
0.5%  →  Operator buffer
0.25% →  Leaderboard campaigns
```

The founder receives less than 1% of network mint via this path, with the rest of the founder allocation coming from the Operator Pool (real bills paid). This is structurally conservative on founder accumulation while keeping the 5% maturity target reachable.

### 17. Burn, escrow, and sinks

One of the most important clarifications in the economy is the distinction between **burn** and **escrow**. Most token failures come from blurring this line.

#### 17.1 Burn (permanent destruction)

A joule is burned when it is intentionally destroyed as payment for a protocol action. Once burned, it cannot be unburned.

| Action | Burn |
|---|---|
| Score a photo (4 critics) | Per measured cost (calibration target) |
| Re-score with additional agent | Per agent in registry |
| Boost a post visibility | 20 kJ + reach multiplier |
| Create a custom AI agent | 50 MJ (one-time registration) |
| Premium actions (Phase 1+) | Per action registry |

#### 17.2 Escrow (conditional, returnable)

A joule is escrowed when it is temporarily locked pending an outcome. **An escrowed joule is not a burn.**

The canonical example is the rating stake.

| Outcome | What happens to the 5 kJ stake |
|---|---|
| Rating in consensus IQR | Returned + 3 kJ bonus (from Network Pool) |
| Rating outside IQR but within 1× | Returned, no bonus |
| Rating wildly off (>1× IQR) | 50% slashed (burned), 50% returned |
| Timing bonus (first 10% of window, accurate) | Returned + 6 kJ bonus |

Slashed joules are **destroyed**, not recycled. This keeps the supply accounting simple and the deflationary pressure honest.

#### 17.3 Edge cases (locked)

**Failed agent calls**: If an agent times out or returns an error during multi-agent scoring, the user is debited only for successful agent responses. Failed calls do not bill the user and do not mint to the network. The photo gets a partial AI consensus, flagged in the UI.

**Starter faucet**: New users receive 500 kJ on signup. These joules come from the **Operator Pool** as a transfer (not a mint). The founder pre-funds the faucet pool by paying for compute, so the joules existed before they went to the new user. Effective founder cost per Genesis Miner: 500 kJ × $0.24/MJ = $0.12.

**Refunds and rollbacks**: If a system error requires reversing a transaction, the reversal is a logged ledger event with a `reverses_ref` field pointing to the original receipt. Both events remain in the append-only history.

#### 17.4 Why burn matters

Burn creates scarcity. It aligns activity with cost. It makes supply mathematically checkable:

```
TOTAL_SUPPLY(t) = TOTAL_MINTED(t) - TOTAL_BURNED(t)
```

This must hold at every moment. If it ever doesn't, the ledger is broken. This is the load-bearing accounting invariant.

### 18. The Treasury Receipt Protocol (TRP)

This is where the public economy connects to the stronger protocol claim:

> If real dollars are continuously being spent to run the protocol, there should be a disciplined way for qualifying spend to appear inside protocol accounting.

Not every expense should create issuance. Only qualifying protocol-compute and protocol-infrastructure spend should do so.

#### 18.1 Receipt classification

Treasury receipts are classified as follows:

| Class | Description | Mintable? |
|---|---|---|
| **Class A** | Direct inference spend (model API usage tied to protocol operation) | Yes — Operator + Treasury Pool |
| **Class B** | Direct protocol compute and storage (hosting, databases, queues, workers, CDN) | Yes — Operator + Treasury Pool |
| **Class C** | Development and experimentation (founder/operator tooling, testing, protocol iteration) | Yes — Operator Pool only |
| **Class D** | Subsidized but non-mintable overhead (email, analytics, monitoring) | No |
| **Class E** | Non-qualifying spend (marketing, legal, accounting, founder time) | No |

#### 18.2 Conversion policy

```
USD_per_MJ = 0.24
MJ_r = qualifying_amount_usd_r / USD_per_MJ
```

This is a treasury accounting coefficient, not a redemption promise and not a market price.

#### 18.3 Qualifying ratios

Within each class, individual receipts have a qualifying ratio that determines what fraction creates issuance:

| Receipt type | Qualifying ratio | Class |
|---|---|---|
| Anthropic / OpenAI / Google API direct inference | 100% | A |
| Self-hosted GPU rental | 100% | A |
| Vercel, Neon, Railway, CDN, storage | 50% | B |
| Claude Code, Cursor, Codex, ChatGPT subscription (when material to protocol) | 100% (amortized over 12 months) | C |
| Email (SendGrid, Postmark, Resend) | 25% | B |
| Monitoring and observability | 25% | B |
| Domain registration | 100% (one-time) | B |
| Marketing | 0% | E |
| Legal, accounting, admin | 0% | E |
| Founder time | 0% | E |

Qualifying ratios are governance parameters. They are reviewed annually and require attestor committee approval to change.

#### 18.4 Split policy

**Class A and B** receipts:

```
80% → Operator Pool
20% → Treasury Pool
```

**Class C** receipts:

```
100% → Operator Pool
```

This preserves a clean distinction: founder/operator-backed protocol work flows mostly to Operator Pool (founder accumulation), with a slice going to Treasury (protocol commons). Development tooling stays entirely in Operator Pool.

### 19. The treasury receipt object

Every qualifying expense produces a treasury receipt with at minimum:

```
{
  "receipt_id":         "trp_2026_04_08_anthropic_001",
  "provider":           "anthropic",
  "provider_category":  "inference_api",
  "classification":     "A",
  "invoice_ref":        "INV-2026-04-A91842",
  "invoice_hash":       "sha256:...",
  "billing_period":     "2026-04-01 to 2026-04-08",
  "amount_native":      "USD 247.83",
  "amount_usd":         247.83,
  "qualifying_ratio":   1.00,
  "qualifying_usd":     247.83,
  "conversion_coef":    0.24,
  "mj_equivalent":      1032.6,
  "mint_split": {
    "operator_pool_kj": 826080,
    "treasury_pool_kj": 206520
  },
  "beneficiary_wallet": "founder_operator_001",
  "proof_bundle_hash":  "sha256:...",
  "settlement_batch":   "2026-04-08-batch-001"
}
```

The protocol may keep raw invoices private while publishing receipt metadata and hashes publicly. This allows public auditability without mandatory disclosure of every private business document.

### 20. Settlement artifacts

Treasury-backed issuance does not happen silently.

Receipts are grouped into **settlement batches**. A settlement batch is the canonical public artifact that explains:

- Which receipts were included
- Which receipts were excluded (and why)
- How qualifying ratios were applied
- Which conversion coefficient was used
- How much was minted, to which pools
- Which wallets received issuance

Each batch is **signed**, **published** to `github.com/joulesgram/protocol/settlements/`, and **chained** to the previous batch by hash. This creates an append-only public history. It is not a conventional blockchain, but it is intentionally **blockchain-like in auditability**: ordered history, tamper evidence, reproducibility, public verification.

### 21. Anti-abuse rules

A receipt-based economy only works if abuse is explicitly prevented.

1. **No duplicate invoices.** The same invoice hash cannot be settled twice.
2. **No double classification.** The same spend cannot be counted twice under different receipt objects unless the split is explicit and qualifying ratios sum to at most 1.0.
3. **No mixed-bill inflation.** Only the qualifying fraction of a mixed bill may create issuance.
4. **No direct public inflation from development tooling.** Class C spend is Operator Pool only.
5. **Forward-only policy changes.** Changes in treasury coefficients or classification policy apply only to future batches, never retroactively.
6. **No receipt, no mint.** Treasury-backed issuance requires a valid receipt and a settlement batch.
7. **No retroactive re-classification.** Once a receipt is settled in a batch, its class and qualifying ratio cannot be changed.
8. **No founder cap override.** When the founder cap (5%) is reached, accumulation pauses. There is no manual override.

### 22. Mathematical invariants

The system must satisfy the following at all times:

1. **No orphan issuance.** Every minted joule points to a genesis record, treasury receipt, operator receipt, or network receipt.
2. **No phantom destruction.** Every burned joule points to a protocol action.
3. **Escrow is not burn.** Locked balances are represented separately from destroyed balances.
4. **Ledger reproducibility.** Any account balance can be recomputed from ledger entries alone.
5. **Supply identity.** `Total Supply = Genesis + Operator Mint + Network Mint - Burns`
6. **Founder cap discipline.** Founder accumulation halts when founder ratio exceeds 5%.
7. **Receipt lineage.** Every treasury-backed issuance points to a hashed receipt bundle and a settlement artifact.
8. **Append-only history.** Past Merkle roots and settlement batches are never deleted or rewritten.

These eight invariants are tested daily by an open-source ledger checker. If any of them fail, the operator publishes an incident report within 24 hours and the protocol enters maintenance mode until the integrity is restored.

---

## Part IV — The Five-Phase Roadmap

The roadmap is sequenced by **what has to be true**, not by calendar time. A phase that takes 6 months in the bull case may take 18 months in the realistic case. The document is honest about that.

### 23. Phase 0 — Bootstrap (now → 1,000 users)

**Trigger**: Public launch of joulegram.com with this whitepaper committed to GitHub.

**Exit condition**: 1,000 active users (≥5 receipts in past 14 days) + 30 days of clean daily Merkle root publication + zero violations of the constitutional rule.

#### 23.1 Goals

1. Get to user #100 with the integrity story intact and the Genesis Miner cohort permanently locked in
2. Calibrate every parameter currently estimated (photo scoring cost, agent token counts, energy coefficients)
3. Prove the daily Merkle root + TRP settlement pipeline runs without missing days
4. Make the four AI critics good enough that people share screenshots of their critiques

#### 23.2 What ships

- This whitepaper, committed
- Genesis Manifest published with the canonical 25 MJ allocation
- Receipt schema with `energy_attestation: "L0"` field
- Daily Merkle root publication script + signed roots in `merkle-roots/`
- TRP v0.1 daily settlement artifacts
- The four AI critics, calibrated
- The three loops (Verdict, Judge, Humans-vs-AI)
- Cohort badges (Genesis Miner / Pioneer / Early Builder / Founding Citizen)
- Activity multiplier (decay over inactivity)
- Direct referral with anti-abuse (5 distinct raters required for bounty)
- Public FAQ addressing the three reviewer critiques

#### 23.3 Founder responsibilities

1. Audit and publish Genesis Pool before user #100
2. Sign every Merkle root, every day, no exceptions
3. Personally onboard users #2 through #100
4. Run the four-critic calibration suite (100 photos, measure actual token counts)
5. Pay every infrastructure bill from personal funds, log every payment in TRP same-day
6. Respond publicly to reviewer critiques using the canonical answers in this whitepaper
7. Publish the weekly transparency post every Sunday

#### 23.4 What early users can do — Tier 1 (critical)

1. **Sign up before user #100 closes.** The Genesis Miner badge is permanent and limited. After user #100 (or 90 days from launch, whichever comes first), no user will ever earn it again.

2. **Post genuinely.** Don't post for joules. Post your best photos. The four critics will tell you what's good and the network will reward what others want to rate. Joulegram is meritocracy plus skin in the game; gaming it dilutes your future position.

3. **Rate accurately.** Honesty compounds. A Genesis Miner who rates accurately for 12 months earns vastly more than a Miner who rates randomly. The math rewards real taste.

4. **Refer one person you'd want to drink coffee with.** Direct referrals are capped at 100 per user. Quality over quantity. Bring people who will participate, not numbers.

#### 23.5 What early users can do — Tier 2 (high-leverage)

5. **File bugs on `github.com/joulesgram/protocol`.** Phase 0 has bugs. Finding them is bootstrapper work and qualifies for Bootstrapper Pool rewards.

6. **Write a public review.** Twitter, Substack, your blog, your group chat. The protocol's distribution problem is bigger than its technology problem. A thoughtful Genesis-Miner write-up is worth more than 1,000 paid impressions.

7. **Suggest the fifth AI critic personality.** The four current critics cover minimalism, color, street, and technical. Adopted suggestions earn a Bootstrapper bonus.

8. **Bring a photographer friend who isn't on social media.** The hardest cohort to reach is good photographers who hate Instagram. They are the protocol's natural audience.

#### 23.6 What early users can do — Tier 3 (long-term)

9. **Start designing the custom agent you'll build at Phase 1.** When user-created agents ship, the first 100 third-party agents will define the network's aesthetic culture. If you have an opinion about visual quality in any domain, you can be one of them.

10. **Draft a JAP integration proposal for your industry.** Phase 1 will fund the first three accepted proposals through the Bootstrapper Pool (500 MJ each). Code review, content moderation, medical imaging, legal research — pick something where AI judgment is currently a vendor black box.

#### 23.7 Metrics that matter

- **User #100 timestamp** (the most important single number)
- **Daily active users** (target: 100 at end of phase, climbing to 1,000)
- **7-day rating retention** (% of users who rate ≥5 photos in week after first post)
- **Receipts per user per day** (target: 5+ at steady state)
- **Daily Merkle root publication rate** (target: 100%)
- **Ledger integrity check** (passes every day, no exceptions)

#### 23.8 Phase 0 risks

1. **Constitutional rule violation** — biggest risk. Mitigation: founder personally signs every root; script is open source; logs are reproducible.
2. **Founder burnout** — solo founder, heavy non-delegable responsibilities. Mitigation: protect the daily Merkle root above all else; everything else can slip.
3. **Critics not fun enough** — consumer wedge fails. Mitigation: ruthless calibration of agent personas in first 30 days based on what users actually share.
4. **Genesis Miner cohort gets sybil-attacked.** Mitigation: anti-abuse on referral bounty, rate-limiting on signup, soft KYC before user #100.

### 24. Phase 1 — Federation (1,000 → 10,000 users)

**Trigger**: Phase 0 exit conditions met.

**Exit condition**: 10,000 active users + 3-of-5 attestor committee operational + first non-Joulegram JAP integration shipped + 90 days of clean federated Merkle roots.

#### 24.1 Goals

1. Move from single-operator to federated attestation
2. Open agent creation to users (Beacon tier unlock at 100k joules earned)
3. Ship the first non-Joulegram JAP integration
4. Reach L1 energy attestation with at least one cloud provider

#### 24.2 What ships

- 3-of-5 attestor committee with public infrastructure
- Custom agent creation via Beacon-tier unlock
- Public JAP API endpoint at `api.joulegram.com/jap/v1`
- Agent fingerprinting and verification (per SPEC §5)
- Provider-attested energy where available (L1)
- First protocol grant program ($50k-$100k from treasury for third-party developers)
- Formal `TREASURY_SPEC.md` published

#### 24.3 What early users can do

**Critical**:
- **Apply to be an attestor.** The first five attestors are the most important post-genesis users. Strong technical chops + willingness to run independent infrastructure. Genesis Miners get priority.
- **Build a custom agent and ship it.** First 100 third-party agents define network aesthetics. Compounding accuracy rewards.
- **Build a JAP integration in your industry.** Bootstrapper bonus 500 MJ for the first third-party shipped.

**High-leverage**:
- Refer technical builders, not just photographers
- Run a public agent leaderboard (Substack, Twitter)
- Translate the spec into non-English languages (100 MJ each)

**Long-term**:
- Practice running a shadow attestor for Phase 2 permissionless attestation
- Identify your Phase 2 protocol contribution

#### 24.4 Metrics

- Attestor uptime (target: 99.9%)
- Federation health (% of roots with full 5-of-5 signatures)
- Custom agents shipped (target: 50+)
- Third-party JAP integrations live (target: 3+)
- Provider-attested receipts as % of total (target: 30%+)

### 25. Phase 2 — Permissionless (10,000 → 100,000 users)

**Trigger**: Phase 1 exit conditions met + first regulator inquiry about JAP receipts (this is a *good* sign and is the actual trigger).

**Exit condition**: Permissionless attestor network with 50+ active attestors + 10+ third-party JAP integrations live + L2 energy attestation across major providers + first non-photo Joulegram client shipped.

#### 25.1 Goals

1. Make attestation permissionless (anyone can run an attestor by staking joules; slashing for misbehavior is real)
2. Expand JAP beyond photos (multiple production clients)
3. L2 energy attestation across major cloud providers
4. Treasury becomes self-sustaining (inflows ≥ outflows)

#### 25.2 What early users can do

**Critical**:
- **Run a permissionless attestor.** Stake joules, sign Merkle roots, earn fees. This is when joules become genuinely productive.
- **Ship a JAP client in a vertical you understand.** Code review, contract analysis, medical imaging, drug screening, ad approval — pick something where AI judgment is currently a vendor black box and replace it with verifiable receipts. Bootstrapper bonus 500 MJ to 5 GJ.
- **Become a calibration consortium member.** L2 attestation requires running benchmark suites against new models monthly.

**High-leverage**:
- Build agent reputation across multiple clients (cross-domain identity)
- Write the JAP technical literature (a book, course, or series)
- Become a treasury committee member (3-of-5 multisig)

**Long-term**:
- Start a JAP-native business — a company that exists because JAP exists

### 26. Phase 3 — Hardware Attestation (100,000 → 1,000,000 users)

**Trigger**: Phase 2 exit conditions + first hardware vendor shipping TEE-based inference attestation in production silicon.

**Exit condition**: L3 energy attestation as default for major cloud providers + 1,000+ permissionless attestors + 50+ JAP clients in production + transferability decision made (yes or no, with legal cover).

#### 26.1 Goals

1. L3 hardware attestation becomes default
2. Resolve transferability question (yes with legal wrapper, or no in perpetuity — either is fine, indecision is what kills protocols)
3. JAP becomes a category, not a project
4. Network supply approaches 1 PJ

#### 26.2 What early users can do

By Phase 3, the user base is large enough that "what you can do" looks like advice for any large open ecosystem:
- Hold or sell, with eyes open
- Fund the next generation of JAP clients via Bootstrapper grants (Phase 3 holders are wealthy in joules)
- Run for foundation governance (Genesis Miners with continuous activity have legitimacy)
- Write the history (Phase 3 is when the early-day stories become valuable cultural artifacts)

### 27. Phase 4 — Standard (1,000,000+ users)

**Trigger**: Phase 3 exit conditions met. JAP is the receipt format used by some large fraction of consequential AI judgments globally.

**Exit condition**: Permanent. Phase 4 is the steady state.

JAP receipts on every consequential AI judgment. Loan approvals: JAP receipt. Medical diagnoses: JAP receipt. Content moderation: JAP receipt. Resume screening: JAP receipt. Drug discovery candidate filtering: JAP receipt. Code review: JAP receipt. Legal citation lookup: JAP receipt.

The unit of account is the joule. The receipt format is JAP. The trust model is L3/L4 hybrid (TEE-attested for critical work, ZK-proven for the highest-stakes work, coefficient-based for everything else). The protocol's treasury is a non-profit foundation. The founder is on the board. Genesis Miners are honored ancestors who occasionally show up at conferences and tell stories.

---

## Part V — The Trillion-Dollar Scenario

### 28. Network valuation framework

The protocol publishes three valuation numbers in every monthly transparency report:

#### 28.1 Replacement Compute Value (RCV) — the floor

```
RCV(t) = TOTAL_SUPPLY(t) × JOULE_USD_BASIS_CURRENT
```

The cost to reproduce the network's compute basis from scratch by buying inference at peg. Cannot be faked. This is the unfalsifiable physics number.

#### 28.2 Live Compute Purchasing Power (LCPP) — the utility value

```
LCPP(t) = LIQUID_SUPPLY(t) / CURRENT_INFERENCE_COST_PER_KJ
```

How much current inference one joule can buy on the open market. Useful for users who think of joules as credit for AI judgment.

#### 28.3 Network Utility Value (NUV) — the strategic value

```
NUV(t) = a × RCV(t) + b × ANNUALIZED_PROTOCOL_REVENUE(t) + c × DISCOUNTED_FUTURE_DEMAND(t)
```

Where weights `a`, `b`, `c` are scenario parameters. This is the speculative number. Not a promise. A scenario.

### 29. Network value at each scale

| Network supply | Floor (RCV at $0.24/MJ) | Realistic market (10×) | Trillion-dollar scenario (1000×) |
|---|---|---|---|
| 1 GJ (1k users) | $240 | $2,400 | n/a |
| 100 GJ (10k users) | $24,000 | $240,000 | n/a |
| 10 TJ (100k users) | $2.4M | $24M | $2.4B |
| 1 PJ (1M users) | $240M | $2.4B | $240B |
| 1 EJ (10M+ users + third-party JAP) | $240B | $2.4T | **$240T** |

### 30. The trillion-dollar scenario

The trillion-dollar scenario requires JAP to become the receipt layer for AI judgment globally. What has to be true:

- Every consequential AI inference is producing a JAP-compliant receipt
- Major regulators (EU, US, India, China) explicitly accept JAP receipts as evidence
- Major insurance companies require JAP receipts to underwrite AI liability
- Major enterprises use JAP receipts for internal AI audit trails
- Major hardware vendors ship JAP-compatible TEE attestation by default
- Major cloud providers offer JAP attestation as a standard product
- The protocol has outlived multiple generations of clients, model architectures, and chip architectures

### 31. The math at scale

If the network reaches 1 EJ of supply with 10× market premium:

| Holder type | Allocation | Floor value | Market value (10×) |
|---|---|---|---|
| Founder (5% cap) | 50 PJ | $12B | $120B |
| Average Genesis Miner (~1/99 of cohort allocation) | ~10 GJ | $2.4M | $24M |
| Active Pioneer (top quartile) | ~5 GJ | $1.2M | $12M |
| Active Early Builder | ~1 GJ | $240k | $2.4M |

These numbers are not promises. They are the math of what would happen if JAP becomes what it could become. Probability is low. Asymmetric upside is the entire point.

### 32. What success looks like in human terms

Mohit will have built the receipt format that humanity uses to verify AI judgment. Chosen, in the founding moments, to share that wealth with the people who showed up early and contributed. Built it in public, on AGPL, with the constitutional rule holding from day one. Stayed honest about the limitations at every phase. Earned 5% of the protocol's value not by gifting himself the share but by paying for the compute that built it.

That is the kind of story that gets told for a long time.

Genesis Miners will have trusted the protocol when it had 8 users. Posted, rated, referred, built. Held through Phase 0's confusion, Phase 1's transitions, Phase 2's growth, Phase 3's politics. Some sold early. Some held all the way. Each contributed in their own way, and each is structurally rewarded by the math.

That, also, is the kind of story that gets told for a long time.

---

## Part VI — Honesty and Limits

### 33. What this whitepaper is not claiming

This whitepaper does **not** claim:

- That joules are redeemable for dollars
- That the treasury conversion coefficient is a market price
- That all infrastructure cost maps perfectly to physical energy
- That the protocol is already fully decentralized
- That every future extension has been finalized
- That the trillion-dollar scenario is likely or guaranteed
- That the founder will retain influence post-Phase 3
- That non-determinism in LLMs has been eliminated
- That Phase 0 attestation is trustless

It claims something narrower and stronger:

> Joulegram is building a disciplined, physics-grounded, receipt-backed system for AI judgment, starting with a product people can actually use. Every joule traces to a receipt. Every receipt traces to a real bill. The protocol earns the right to become more open, one phase at a time, by surviving the integrity tests of the previous phase.

### 34. Comparison to prior art

| Project | What it does | What JAP does differently |
|---|---|---|
| **Bittensor (TAO)** | Decentralized AI inference marketplace, Yuma Consensus rewards model accuracy | TAO incentivizes producing AI; JAP incentivizes verifying AI. Complementary — JAP receipts could be produced by TAO subnets. |
| **Oraichain (Orai)** | AI oracle network, brings AI inference results onto blockchain | Orai puts AI on a chain. JAP creates a verifiable receipt format that any chain (or no chain) can consume. JAP is the format; Orai is one possible client. |
| **SingularityNET** | AI marketplace with reputation and PoR/PoI hybrid | SingularityNET is a marketplace. JAP is a receipt protocol. SingularityNET services could produce JAP receipts. |
| **Chainlink (LINK)** | Oracle network with committee-based attestation | Closest architectural cousin. JAP follows LINK's playbook for early phases (committee), then specifies the path beyond it (TEE, ZK) in a way LINK has not. |
| **EigenLayer** | Restaking, economic security as a service | One possible substrate for JAP attestor staking in Phase 2+. Not a competitor. |

JAP is positioned as the **receipt layer underneath** other AI-related protocols. The other projects are inference, marketplaces, oracles, and security primitives. JAP is the format they all need but none of them currently provide.

### 35. The narrative in one paragraph

Bitcoin grounded money in physics. Ethereum grounded computation in physics. Joulegram grounds AI judgment in physics, makes that judgment socially engaging, and then turns the receipts from that judgment into a public, auditable economic system. The founder is honored because he created the primitive. Early users are rewarded because they create the first network. Active users can outrun passive users because merit must beat chronology. And every serious claim the protocol makes eventually reduces to a receipt, a batch artifact, and a ledger entry.

### 36. Closing

There is only one genesis.

There are only a handful of people who will ever be able to say they were there when verifiable AI judgment first became a live network.

Joulegram is designed so that:
- the founder is properly honored,
- the early users are properly rewarded,
- the active users are properly empowered,
- and the receipts eventually prove what the protocol claims.

That is the bet.

---

## Appendix A — Glossary

| Term | Definition |
|---|---|
| **JAP** | Joulegram Agent Protocol — the receipt format for AI judgment |
| **Joule (J)** | The protocol's base unit of energy-equivalent accounting |
| **MJ / GJ / TJ / PJ / EJ** | Megajoule (10⁶), Gigajoule (10⁹), Terajoule (10¹²), Petajoule (10¹⁵), Exajoule (10¹⁸) |
| **L0/L1/L2/L3/L4** | Energy attestation levels — coefficient, provider-attested, calibrated, TEE-attested, ZK-proven |
| **TRP** | Treasury Receipt Protocol — the system for converting fiat spend into receipt-backed issuance |
| **Genesis Pool** | The one-time founder allocation of 25 MJ. Locked, finite, non-repeatable. |
| **Operator Pool** | Receipt-backed issuance tied to ongoing protocol operations spend |
| **Network Pool** | Activity-based issuance from user participation |
| **Attestor** | An entity authorized to sign Merkle roots and settlement batches |
| **Cohort** | A user category determined by signup order (Genesis Miner, Pioneer, Early Builder, Founding Citizen) |
| **Settlement batch** | The canonical public artifact recording a treasury issuance event |
| **Merkle root** | A cryptographic commitment to all receipts in an epoch, signed by attestors |

## Appendix B — Versioning and Amendments

This is **Whitepaper v1.0**. It supersedes all prior drafts of Joulenomics (v1, v2) and Roadmap.

Amendments require:
- A pull request to `github.com/joulesgram/protocol/WHITEPAPER.md`
- A 30-day public review period
- Approval by the attestor (Phase 0: founder; Phase 1+: 3-of-5 committee)
- A signed commit referencing the prior version's hash

Past versions are never deleted. The full history of every economic rule the protocol has ever operated under is preserved in `git log`, forever.

**Section 5 (the constitutional rule) cannot be amended under any conditions.** Section 14.4 (the 5% founder cap) cannot be amended without unanimous attestor approval. All other sections can be amended through the standard process.

---

*Mohit Lalvani · Founder, User #1, Genesis Miner*
*Goa, India · April 9, 2026*
*joulegram.com · github.com/joulesgram*
