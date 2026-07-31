# Conclusion

The current live score is **8/10**. This candidate does not claim that the
score has changed.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | Preserved byte-for-byte from the live judged revision |
| 2 | 2 | 2 | HIGH | VERIFIED | Preserved byte-for-byte from the live judged revision |
| 3 | 2 | 2 | HIGH | VERIFIED | Preserved byte-for-byte from the live judged revision |
| 4 | 1 | 2 | MEDIUM | VERIFIED | Lean checks the universal deduction; exact matrix-level realization of its architecture premises is not yet in Lean |
| 5 | 1 | 2 | HIGH | VERIFIED | Lean checks the arbitrary compact-space density theorem and both compact-cover steps |

- Previous live judged score: `8/10`
- Conservative projected score range: `9–10/10`
- Best-supported possible score: `10/10` **forecast only**
- Changed since the judge result: Claims 4 and 5 only
- BLOCKED claims: none, but Claim 4 has the formalization boundary stated above
- Exact command: `uv run --frozen python run_reproduction.py`
- Formal evidence run: [HF Job](https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f)
- Evidence SHA: `3820f7a5601f0d4e52d1936ce045303796519f8d`
- Compute: HF `cpu-upgrade`; 64 logical CPUs visible, `LAKE_JOBS=1`, 164.07 s

## Reproducibility

The [Claim 4](#/claim-4-current) and [Claim 5](#/claim-5-current) pages expose
the exact theorem contracts, Lean sources, raw kernel result, independent
checker, negative controls, fixed command, pinned environment, and limitations.
The formal verifier exits nonzero on a build failure, forbidden proof token,
unsafe axiom, or a negative control that unexpectedly compiles.

All files from the live 8/10 Space revision remain present. The older sampled
pages remain available as
[historical evidence](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/tree/main/pages);
they are not the current verifier. The previous full report and five figures
remain in the [GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers).

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/claim-1-current) | yes | yes | yes | yes | yes | yes | unchanged, release-ready |
| 2 | [Claim 2](#/claim-2-current) | yes | yes | yes | yes | yes | yes | unchanged, release-ready |
| 3 | [Claim 3](#/claim-3-current) | yes | yes | yes | yes | yes | yes | unchanged, release-ready |
| 4 | [Claim 4](#/claim-4-current) | yes | yes | yes | yes | yes | yes | release-ready; MEDIUM architecture-premise risk |
| 5 | [Claim 5](#/claim-5-current) | yes | yes | yes | yes | yes | yes | release-ready |

## Evaluator-blind red team

The artifact-only reviewer opened `README.md`, `logbook.json`,
`pages/index.md`, the executive summary, all five canonical claim pages, and
this conclusion, then followed every raw evidence link. It found:

- zero missing canonical pages or raw links;
- zero secret-pattern hits;
- all 89 files from the live 8/10 revision still present;
- zero unallowlisted changes to protected historical files; and
- exact live hashes retained for Claims 1–3.

The review was repeated after fixing the initial audit's treatment of directory
links and the generated upload manifest. The repeated audit passed.
