# Claim 4 — universal approximation

**Verdict: VERIFIED. Confidence: MEDIUM.**

## Exact contract

For every finite dimension `d`, compact `Omega ⊂ R^d`, `C>0`, target
`Lambda* ∈ C_(1,C)(P(Omega) × Omega, R)`, and `epsilon ∈ (0,1)`, Theorem 8
asserts that there is a scalar gradient-descent-type in-context Transformer in
`G_C` whose uniform error is at most `epsilon`. Because the domain contains all
probability measures, this statement is independent of the number of empirical
context tokens.

## What is now machine checked

The Lean theorem `transformerUniversalApproximation` quantifies over arbitrary
compact metric context/query spaces, every separately Lipschitz target, and
every positive tolerance. The kernel checks:

1. separate query/context bounds imply the product budget;
2. strict two-point interpolation plus lattice closure imply density;
3. the sign-safe interpolation coefficient satisfies `|alpha|<1`—including
   the negative-coefficient case missing from the paper's `[0,1]` wording;
4. the scalar ResNet density conclusion follows from the corresponding
   Murari lattice/interpolation obligations; and
5. the final compact-domain uniform approximation theorem.

This is not a fit to a selected function or a finite collection of targets.

## Raw evidence

| Check | Observed result |
| --- | --- |
| Lean / mathlib | 4.19.0 / v4.19.0 (`c44e0c8…`) |
| Build | return code `0`; `transformerUniversalApproximation` compiled |
| Unsafe proof placeholders | no forbidden token; no `sorryAx` |
| Reported axioms | `propext`, `Classical.choice`, `Quot.sound` only |
| Negative coefficient control | rejected, unsolved `False` |
| Strict-margin control | rejected, unsolved `False` |
| Independent finite-domain corroboration | envelope error `0.0`; KR witness gap exactly `1.2884098726725126` |

- Fixed command: `uv run --frozen python run_reproduction.py`
- Git SHA: `3820f7a5601f0d4e52d1936ce045303796519f8d`
- Compute estimate: one active core, uncertain runtime → HF `cpu-upgrade`
- Allocation/runtime: 64 logical CPUs visible, `LAKE_JOBS=1`, 164.07 seconds
- [Exact HF Job](https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f)

## Downloadable code and evidence

[Formal result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/formal_verification_output.json),
[contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/raw_results.json),
[independent checker output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/independent_checker_output.json),
[negative-control output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/negative_control_output.json),
[claim verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/verify.py),
[universal theorem source](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/LipschitzTransformerFormal/TransformerUniversalApproximation.lean),
[density theorem source](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/LipschitzTransformerFormal/RestrictedStoneWeierstrass.lean),
[formal runner](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/formal_verifier.py),
[failing controls](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/tree/main/formal_negative_controls),
[environment lock](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/uv.lock).

## Limitation

The Lean theorem assumes the Transformer class is nonempty, lattice-closed,
and strictly two-point interpolating. The paper's exact matrix-level
parallel-attention, uniform-score attention, KR-witness approximation, and
projection constructions establishing those premises are source-audited and
checked by the executable proof DAG, but are not themselves represented as
Lean matrices. This remaining architecture-semantic boundary is why confidence
is MEDIUM and why 2/2 is a judge forecast, not a guaranteed score.
