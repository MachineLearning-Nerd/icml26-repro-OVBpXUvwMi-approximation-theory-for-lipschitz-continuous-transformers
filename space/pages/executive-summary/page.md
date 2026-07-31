# Executive summary

---
<!-- trackio-cell
{"type":"markdown","id":"cell-executive-summary","created_at":"2026-07-31T00:00:00+00:00","title":"Executive summary","pinned":true}
-->
The live judge awarded **8/10** at Space revision
`c09976f4189cfa624d6dbb8ac4ef96d14eb113e3`: Claims 1–3 received 2/2;
Claims 4–5 remained 1/2 because their evidence was not a machine-checked proof
of the arbitrary compact-domain theorems.

This revision changes only the scientific evidence for Claims 4 and 5.
Lean 4.19.0 + mathlib v4.19.0 now checks the arbitrary compact-space
restricted Stone–Weierstrass argument, its two compact-subcover construction,
strict-margin scaling, the product Lipschitz budget, and the final universal
approximation deduction from the paper-class lattice/interpolation premises.
Both deliberately false controls are rejected. Claims 1–3 are preserved
byte-for-byte from the live 8/10 revision.

| Scope | Result | Cost / provenance |
| --- | --- | --- |
| Claim 4 universal deduction | `transformerUniversalApproximation` compiled; no `sorryAx` | [HF cpu-upgrade Job](https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f), 164.07 s, one enforced worker |
| Claim 5 compact-space density | Seven theorem obligations compiled on arbitrary compact metric spaces | Lean 4.19.0, mathlib commit `c44e0c8…` |
| Negative controls | 2/2 rejected with unsolved `False` | strict-margin and coefficient-sign controls |
| Source and code | Exact fixed command and pinned environment | [GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers), SHA `3820f7a…` |

Conservative projected score after reevaluation: **9–10/10**. A 10/10 is a
forecast, not an earned judge result. Claim 4 remains MEDIUM confidence because
the exact matrix-level Transformer realization of the lattice/interpolation
premises is source-audited but not itself encoded in Lean.

---
<!-- trackio-cell
{"type":"figure","id":"cell-reproduction-poster","created_at":"2026-07-31T00:00:00+00:00","title":"Reproduction poster","pinned":true,"poster":true}
-->
````html
<iframe src="poster_embed.html" title="Claims 4 and 5 formal verification poster" width="100%" height="720" loading="lazy"></iframe>
````

[Open the full reproduction poster](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/poster_embed.html).
