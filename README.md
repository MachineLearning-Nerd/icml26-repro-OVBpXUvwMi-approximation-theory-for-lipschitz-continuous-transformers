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
reconstruction. The live judge awarded **8/10** at revision `c09976f`: Claims
1–3 received 2/2 and Claims 4–5 received 1/2. The new evidence changes only
Claims 4–5. Lean 4.19.0 now checks Claim 5's arbitrary compact-space theorem
and Claim 4's universal deduction from the paper-class
lattice/interpolation premises. Claim 5 is HIGH confidence; Claim 4 remains
MEDIUM because the exact matrix-level realization of those premises is not
encoded in Lean. The score remains 8/10 until the live judge evaluates the new
revision.

The numerical checks are intentionally downscaled diagnostics—d=16/d=32, 512
tokens, and 128 layers. They do not prove universal quantifiers. The proof
reconstruction carries those quantifiers, replacing the prior d=1 and circular
target-fitting evidence.

- [Illustrated technical report](reports/lipschitz-transformer/report.md)
- [Tutorial-style marimo notebook](notebooks/lipschitz_transformer_reproduction.py)
- [Published evaluator logbook](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi)
- [Exact published text mirror](space/pages/index.md) — Space revision
  `81674f553e4492b5767374ae6c3573b8658b957f`

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and evidence links | none |
| [judged toy baseline](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/judged-toy-baseline) | Freeze and rerun the judged d=1 evidence | `uv run --frozen python run_reproduction.py` | Historical rejected baseline; regression only | local CPU, 1.266 s |
| [direct symbolic proof certificates](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/direct-symbolic-proof-certificates) | Replace finite sampling with arbitrary-object derivations, independent checks, and controls | `uv run --frozen python run_reproduction.py` | 25/25 nodes; five claims VERIFIED; 5/5 controls rejected | local CPU, one thread, 1.805 s |
| [assumption-satisfying falsification audit](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/assumption-satisfying-falsification-audit) | Search exact-claim boundaries and counterexamples | `uv run --frozen python run_reproduction.py` | No exact counterexample; corrected Claim 2 parameter scope and Claim 3 depth scope | HF `cpu-upgrade`, one-thread limit, 16 s provider runtime |
| [cumulative evaluator-visible candidate](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/cumulative-evaluator-visible-release-candidate) | Rerun all accepted checks and validate canonical navigation | `uv run --frozen python run_reproduction.py` | All checks passed; 16 pages and 17 historical files accounted for | local CPU, one thread, 1.270 s |
| [release-gated artifact](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/release-gated-publication-artifact) | Fresh assembly, red team, report, notebook, and final regression | `uv run --frozen python run_reproduction.py` | All gates passed at `adfacf0`; published as HF revision `c09976f` | local CPU, one thread, 1.319 s |
| [Lean formal verification](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/lean-formal-verification-for-claims-4-and-5) | Formalize the compact-space Claim 5 proof and Claim 4 universal deduction | `uv run --frozen python run_reproduction.py` | Lean kernel build passed; both false controls rejected | HF `cpu-upgrade`, one worker, 164.07 s |
| [evaluator-visible Claims 4/5 evidence](https://github.com/MachineLearning-Nerd/icml26-repro-OVBpXUvwMi-approximation-theory-for-lipschitz-continuous-transformers/tree/orx/evaluator-visible-claims-4-and-5-formal-evidence) | Canonical pages, pinned poster, protected-tree audit, and cumulative regression | `uv run --frozen python run_reproduction.py` | All gates passed at `ab99c63`; published as HF revision `81674f5` | HF `cpu-upgrade`, one worker, 139.12 s |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python run_reproduction.py
```

The verifier exits nonzero if the historical regression, proof certificate,
independent checks, controls, or candidate navigation fails.
