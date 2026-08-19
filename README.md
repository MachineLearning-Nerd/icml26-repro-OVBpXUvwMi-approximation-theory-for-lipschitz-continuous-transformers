# Approximation Theory for Lipschitz Continuous Transformers — independent reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/blob/main/notebooks/lipschitz_transformer_reproduction.py)

Independent reproduction and claim audit for **Approximation Theory for
Lipschitz Continuous Transformers** by Takashi Furuya, Davide Murari, and
Carola-Bibiane Schönlieb.

- Paper: [arXiv:2602.15503](https://arxiv.org/abs/2602.15503)
- Clean repository: [MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers)
- Reproduction entrypoint: `uv run --frozen python run_reproduction.py`
- Published evaluator logbook: [DineshAI/OVBpXUvwMi](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi)
- Exact published text mirror: [`space/pages/index.md`](space/pages/index.md), Space revision `81674f553e4492b5767374ae6c3573b8658b957f`

## What the paper does

The paper proposes gradient-descent-type in-context Transformers whose MLP
and attention blocks are explicit Euler steps of negative gradient flows. The
construction is designed to preserve a 1-Lipschitz query map while allowing a
finite Wasserstein-1 Lipschitz constant with respect to the context measure.
It then proves uniform approximation of scalar in-context maps that have the
same separate Lipschitz constraints, independently of the number of context
tokens.

The attention layer is

\[
\Gamma(\mu,x)=x-\eta\int
\frac{e^{\langle x,Ay\rangle}}{\int e^{\langle x,Az\rangle}d\mu(z)}Ay\,d\mu(y),
\]

with `eta` restricted by the input-domain bound. The approximation theorem is
measure-theoretic: the context is a probability measure, and the proof uses a
restricted Stone–Weierstrass argument plus Kantorovich–Rubinstein witnesses.

## Reproduction status

The verdicts below are scoped to the explicit contracts in
[`space/evidence/current/`](space/evidence/current/). `VERIFIED` means that
the recorded proof/evidence path satisfies that contract; it is not a claim
that a finite numerical experiment proves a universal theorem.

Overall status: `ALL_FIVE_CLAIMS_VERIFIED_SCOPED_CLAIM_4_MATRIX_REALIZATION_MEDIUM_CONFIDENCE`.
Claims 1, 2, 3, and 5 have high-confidence proof or architecture certificates;
Claim 4 is verified at medium confidence because the abstract Lean deduction
assumes paper-class premises whose exact matrix-level realization is
source-audited but not itself encoded as Lean matrices. `publication_allowed=false`,
`score_claim=false`, and `official_author_endorsement=false` until an
independent evaluator judges the public revision.

| Claim | Paper result | Evidence and production path | Verdict |
| --- | --- | --- | --- |
| 1 | Lemma 1: an admissible ReLU Euler MLP layer is 1-Lipschitz | [`proof_verifier.py`](reproduction/proof_verifier.py) checks the gradient, segment Jacobian, PSD spectrum, and piecewise-affine argument; the independent checker exhausts 1,024 activation masks at `d=16`; a non-admissible control is rejected | **VERIFIED · HIGH** |
| 2 | Lemma 2: fixed-parameter attention is query-nonexpansive and context-Lipschitz in `W1` | The certificate derives the tilted covariance Hessian, cocoercive query step, and quotient/KR measure bound; the independent checker uses `d=32`, 512 tokens, and the covariance bound; fixed `(A, eta)` scope and a parameter-boundary control are recorded | **VERIFIED · HIGH** |
| 3 | Lemma 6: finite compositions keep query constant at most one and have a finite context constant | The verifier propagates query, pushforward, and context constants by an exact finite-depth recurrence; the independent check reaches 128 layers with query product `1.0` and finite context constant `3.858201434572288e+17` | **VERIFIED · HIGH** |
| 4 | Theorem 8: every scalar `(1,C)` target on the compact measure/query domain is uniformly approximable | The proof chain combines lattice closure, a KR witness, cited scalar-ResNet density, a uniform-attention integral, and the Claim 5 density lemma; Lean checks the abstract deduction, while the matrix-level realization is independently audited | **VERIFIED · MEDIUM** |
| 5 | Lemma 9: a lattice with strict Lipschitz point separation is dense | Lean checks strict-margin scaling, both compact finite-subcover steps, lattice min/max construction, and the uniform error bound; no fitted target or selected basis is used | **VERIFIED · HIGH** |

The paper's logical order is Claim 5 before Claim 4: Claim 5 is the abstract
density engine applied to the Transformer class in Claim 4. The recorded
release run reported 25/25 proof dependencies, all five claim contracts
passing, and five premise-violating negative controls rejected. The latest
historical live-judge score in the artifacts is `8/10` at revision `c09976f`;
the later Claims 4/5 evidence was published as a new revision and remains
awaiting a fresh judge decision.

## How each claim is produced

The fixed entrypoint runs the historical regression first, then executes the
proof dependency certificate, independent checks, negative controls, and
publication-navigation validation:

```text
run_reproduction.py
├── reproduction/proof_verifier.py       # 25-node symbolic dependency DAG
├── reproduction/independent_checker.py # separate numerical/exact checks
├── reproduction/negative_controls.py    # premise-violating controls
└── reproduction/candidate_validator.py  # evaluator-visible navigation
```

The proof-to-verdict path is:

1. **Claim 1:** differentiate the ReLU potential on each activation segment,
   bound `0 <= WᵀDW <= ||W||²I`, and integrate the segment Jacobian. The
   numerical mask enumeration corroborates the dimension-free derivation.
2. **Claim 2:** identify the attention Hessian with a tilted covariance,
   apply the smooth convex gradient-step bound to the query, and use bounded
   exponentials plus Kantorovich–Rubinstein duality for the context quotient.
3. **Claim 3:** propagate query and context changes through every finite layer
   with the Wasserstein coupling recurrence. Query sensitivity stays at most
   one; the context constant is finite but may grow with depth.
4. **Claim 4:** establish the Transformer-class lattice and strict separation.
   The separation path uses a compact-domain KR witness, scalar ResNet density,
   and an attention layer that computes the required context integral. Apply
   Claim 5 to obtain the uniform approximation theorem.
5. **Claim 5:** scale the target to create a strict Lipschitz margin, construct
   local interpolants, take a finite lattice minimum over one compact cover,
   and a finite lattice maximum over a second cover.

The full derivation is in
[`reproduction/symbolic_derivation.md`](reproduction/symbolic_derivation.md);
each claim's contract, raw result, independent check, negative control, and
limitations are under `space/evidence/current/claim_<n>/`.

## Branches and experiments

`main` is the publication surface. The historical `orx/` names were cleaned
up into the branches below; the complete mapping is in
[`branch-audit.md`](branch-audit.md).

| Clean branch | Purpose | Recorded outcome |
| --- | --- | --- |
| [`audit/judged-toy-baseline`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/audit/judged-toy-baseline) | Preserve the judged `d=1` baseline | Historical regression only; rejected as theorem-level evidence |
| [`audit/direct-symbolic-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/audit/direct-symbolic-proof-certificates) | Replace finite sampling with arbitrary-object derivations and controls | 25/25 proof nodes; five claim contracts verified |
| [`audit/assumption-satisfying-falsification`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/audit/assumption-satisfying-falsification) | Search claim boundaries and counterexamples | No exact-claim counterexample; scope corrections retained |
| [`release/cumulative-evaluator-candidate`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/release/cumulative-evaluator-candidate) | Validate cumulative evidence and canonical navigation | All checks passed; historical and current pages accounted for |
| [`release/release-gated-artifact`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/release/release-gated-artifact) | Assemble the first release-gated report and notebook | All gates passed at `adfacf0`; published Space revision `c09976f` |
| [`formal/claims-4-and-5-lean`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/formal/claims-4-and-5-lean) | Formalize the compact-space density step | Lean kernel build passed; false controls rejected |
| [`release/evaluator-claims-4-and-5`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/release/evaluator-claims-4-and-5) | Publish the current Claims 4/5 evidence | All gates passed at `ab99c63`; Space revision `81674f5` |
| [`integration/published-lean-evidence`](https://github.com/MachineLearning-Nerd/icml26-approximation-theory-lipschitz-continuous-transformers/tree/integration/published-lean-evidence) | Mirror the published Lean evidence onto `main` | Current publication surface; tip `db777b5` before documentation |

## Repository map

- `reproduction/` — executable proof DAG, independent checker, controls, and
  candidate validator.
- `LipschitzTransformerFormal/` — Lean formalization of the density argument.
- `formal_negative_controls/` — Lean counter-controls for missing premises.
- `reports/lipschitz-transformer/` — illustrated technical report.
- `notebooks/` — tutorial-style marimo reproduction notebook.
- `space/evidence/current/claim_<n>/` — claim contracts and evidence ledger.
- `space/pages/` — evaluator-visible current and historical explanations.
- `.openresearch/artifacts/` — protected source audit and release manifests.

## Reproduce

Install the locked environment and run the single verifier:

```bash
uv sync --frozen
uv run --frozen python run_reproduction.py
```

The verifier exits nonzero if the historical regression, proof certificate,
independent checks, negative controls, or candidate navigation fails. The
numeric checks are deliberately downscaled corroboration (`d=16`, `d=32`,
512 tokens, and 128 layers); they do not establish universal quantifiers.

## Citation

```bibtex
@article{furuya2026approximation,
  title         = {Approximation Theory for Lipschitz Continuous Transformers},
  author        = {Furuya, Takashi and Murari, Davide and Schönlieb, Carola-Bibiane},
  journal       = {arXiv preprint arXiv:2602.15503},
  year          = {2026},
  doi           = {10.48550/arXiv.2602.15503}
}
```

Machine-readable citation metadata is also available in
[`CITATION.cff`](CITATION.cff), and the author note is kept separately in
[`AUTHOR_THANK_YOU.md`](AUTHOR_THANK_YOU.md).

## Thank you

Thank you to Takashi Furuya, Davide Murari, and Carola-Bibiane Schönlieb for
the careful theoretical treatment of stability and universal approximation in
measure-valued in-context Transformers. This independent reproduction is
maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd)
as a transparent audit and learning resource; the verdicts above are scoped
to the recorded evidence contracts and are not an endorsement or correction
of the authors' work.
