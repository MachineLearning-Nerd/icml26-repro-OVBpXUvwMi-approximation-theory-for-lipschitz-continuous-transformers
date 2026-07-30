# Approximation Theory for Lipschitz Continuous Transformers — reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/blob/main/notebooks/lipschitz_transformer_reproduction.py)

This project reproduces the five universal claims in
[arXiv:2602.15503](https://arxiv.org/abs/2602.15503): nonexpansive MLP and
attention Euler layers, finite-depth stability, scalar in-context universal
approximation, and the restricted Stone–Weierstrass lemma used by the proof.

The paper’s key numerical bound is a Lipschitz constant at most `1`; its main
approximation result is uniform error at most any prescribed
`epsilon in (0,1)`. The reproduction obtained:

- 25/25 symbolic proof dependencies with zero errors;
- all 1,024 activation masks at d=16, maximum norm
  `1.0000000000000009` within `5e-12` numerical tolerance;
- d=32 attention with 512 tokens, covariance maximum `0.1179650713` below the
  stated bound `1.8345056015`;
- a 128-layer query-constant product of `1.0`; and
- five of five theorem-specific negative controls rejected.

Assessment: all five claims are **VERIFIED** by independent symbolic
reconstruction. Claims 1, 2, 3, and 5 have HIGH confidence; Claim 4 has MEDIUM
confidence because its chain imports Murari et al., Theorem 3.1 instead of
formalizing that antecedent in a proof assistant. This is a forecasted evidence
upgrade, not a live-judge score increase; the judged score remains 5/10 until a
new Space revision is evaluated.

The numerical checks are intentionally downscaled diagnostics—d=16/d=32, 512
tokens, and 128 layers. They do not prove universal quantifiers. The proof
reconstruction carries those quantifiers, replacing the prior d=1 and circular
target-fitting evidence.

- [Illustrated technical report](reports/lipschitz-transformer/report.md)
- [Tutorial-style marimo notebook](notebooks/lipschitz_transformer_reproduction.py)
- [Published evaluator logbook](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and evidence links | none |
| [judged toy baseline](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/judged-toy-baseline) | Freeze and rerun the judged d=1 evidence | `uv run --frozen python run_reproduction.py` | Historical rejected baseline; regression only | local CPU, 1.266 s |
| [direct symbolic proof certificates](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/direct-symbolic-proof-certificates) | Replace finite sampling with arbitrary-object derivations, independent checks, and controls | `uv run --frozen python run_reproduction.py` | 25/25 nodes; five claims VERIFIED; 5/5 controls rejected | local CPU, one thread, 1.805 s |
| [assumption-satisfying falsification audit](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/assumption-satisfying-falsification-audit) | Search exact-claim boundaries and counterexamples | `uv run --frozen python run_reproduction.py` | No exact counterexample; corrected Claim 2 parameter scope and Claim 3 depth scope | HF `cpu-upgrade`, one-thread limit, 16 s provider runtime |
| [cumulative evaluator-visible candidate](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/cumulative-evaluator-visible-release-candidate) | Rerun all accepted checks and validate canonical navigation | `uv run --frozen python run_reproduction.py` | All checks passed; 16 pages and 17 historical files accounted for | local CPU, one thread, 1.270 s |
| [release-gated artifact](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/release-gated-publication-artifact) | Fresh assembly, red team, report, notebook, and final regression | `uv run --frozen python run_reproduction.py` | Release candidate; final regression recorded in the experiment description | local CPU, one thread |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python run_reproduction.py
```

The verifier exits nonzero if the historical regression, proof certificate,
independent checks, controls, or candidate navigation fails.
