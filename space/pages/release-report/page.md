# Release report

- Previous live judged score: `5/10`
- Conservative projected score range after this candidate: `8–10/10`
- Best-supported possible new score: `10/10` **forecast, not a judge result**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Dimension-free spectral proof; exhaustive 1,024-mask check and oversized-step control |
| 2 | 1 | 2 | HIGH | VERIFIED | Covariance/cocoercivity/KR proof; fixed-parameter scope is essential |
| 3 | 1 | 2 | HIGH | VERIFIED | Finite-depth recurrence; context constant may grow with depth |
| 4 | 1 | 2 | MEDIUM | VERIFIED | Full lattice/KR/separation proof; Murari theorem is imported, not proof-assistant formalized |
| 5 | 1 | 2 | HIGH | VERIFIED | Arbitrary-target two-cover proof; non-circular control |

Current total score remains **5/10** until the live judge evaluates a new
revision. All five claims changed from TOY evidence to theorem-level symbolic
verification plus independent checks and controls. No claim is BLOCKED.

## Provenance and compute

- Proof run: SHA `93baf87fa5bc1c062e83ad36604203d87ba911e4`,
  local one-thread CPU, 8 logical CPUs visible, 1.269538 seconds.
- Boundary audit: SHA `1d043ee86ed9baa8db743ad1d4d477d7ece4a949`,
  HF `cpu-upgrade`, 64 logical CPUs allocated, one-thread numerical limit,
  16 seconds provider runtime, 0.249335 seconds measured.
- Exact command on every node:
  `uv run --frozen python run_reproduction.py`.
- Python 3.12; NumPy 2.5.1 from the committed uv lock.
- HF cpu-upgrade list price/cost was not exposed in the run log; no cost is
  invented.

Publication action after all gates: upload the text-only allowlist to the
existing `DineshAI/OVBpXUvwMi` Space, verify the exact revision and hashes,
then mirror reader-facing text to GitHub `main`. No second Space will be
created.
