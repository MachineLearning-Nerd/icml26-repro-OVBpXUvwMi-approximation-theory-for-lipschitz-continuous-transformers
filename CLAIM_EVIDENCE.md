# Claim-to-evidence ledger

Each verdict is produced by the 25-node proof dependency certificate,
independent checks, premise-violating negative controls, and the evaluator
navigation gates. Claim contracts and raw evidence are under
[`space/evidence/current`](space/evidence/current).

| Claim | Verdict | How the verdict is produced | Primary evidence |
| --- | --- | --- | --- |
| C1. ReLU Euler MLP layer | `VERIFIED_SCOPED_HIGH` | Bound the segment Jacobian using the PSD spectrum inequality, integrate the piecewise-affine path, exhaust 1,024 activation masks at `d=16`, and reject an inadmissible control. | [`reproduction/proof_verifier.py`](reproduction/proof_verifier.py) · [`space/pages/claim-1-current/page.md`](space/pages/claim-1-current/page.md) |
| C2. Fixed-parameter attention stability | `VERIFIED_SCOPED_HIGH` | Identify the attention Hessian with a tilted covariance, apply cocoercivity for the query step, and use bounded exponentials plus Kantorovich–Rubinstein duality for the context quotient. | [`space/pages/claim-2-current/page.md`](space/pages/claim-2-current/page.md) · [`space/evidence/current/claim_2`](space/evidence/current/claim_2) |
| C3. Finite-depth composition | `VERIFIED_SCOPED_HIGH` | Propagate query, pushforward, and context constants through the exact finite-depth recurrence to depth 128; query product remains `1.0` and the context constant is finite. | [`space/pages/claim-3-current/page.md`](space/pages/claim-3-current/page.md) · [`space/evidence/current/claim_3`](space/evidence/current/claim_3) |
| C4. Universal approximation | `VERIFIED_SCOPED_MEDIUM` | Combine lattice closure, a KR witness, cited scalar-ResNet density, a uniform-attention integral, and Claim 5; Lean checks the abstract deduction while matrix-level realization remains source-audited. | [`space/pages/claim-4-current/page.md`](space/pages/claim-4-current/page.md) · [`space/evidence/current/claim_4`](space/evidence/current/claim_4) |
| C5. Restricted Stone–Weierstrass density | `VERIFIED_SCOPED_HIGH` | Scale for a strict Lipschitz margin, construct local interpolants, and take finite lattice minima/maxima over compact covers; Lean checks seven theorem obligations and false controls are rejected. | [`space/pages/claim-5-current/page.md`](space/pages/claim-5-current/page.md) · [`space/evidence/current/claim_5`](space/evidence/current/claim_5) |

The fixed entrypoint runs the historical regression, proof DAG, independent
checker, negative controls, and candidate navigation validation. It exits
nonzero if any required contract or release gate fails.

