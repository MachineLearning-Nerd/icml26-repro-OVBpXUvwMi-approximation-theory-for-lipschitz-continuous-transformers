# Claim 5 — restricted Stone-Weierstrass

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact contract

For arbitrary compact metric spaces `U` and `X`, a lattice `L` of separately
`(1,C)`-Lipschitz continuous functions is uniformly dense when it can
interpolate every admissible two-point value pair whose gap is strictly below
`d_X(x,y) + C d_U(u,v)`. The quantifiers range over every admissible target and
every positive uniform tolerance.

Kantorovich–Rubinstein duality is used by the paper to prove the Transformer
class satisfies the separation premise. It is not an assumption of the
abstract density lemma itself.

## What is now machine checked

Lean 4 formalizes the full arbitrary compact-space proof:

1. scale any target strictly toward zero while remaining arbitrarily close;
2. turn the non-strict Lipschitz target inequality into a strict
   two-point budget;
3. use separation to obtain target-relative local interpolants;
4. use compactness for a finite first cover and lattice supremum;
5. use compactness again for a finite second cover and lattice infimum; and
6. combine the two approximation errors by the triangle inequality.

No chosen target, target-derived basis, least-squares fit, finite query set, or
formula-selected approximation budget appears in the theorem.

## Raw evidence

| Check | Observed result |
| --- | --- |
| Lean / mathlib | 4.19.0 / v4.19.0 (`c44e0c8…`) |
| Formal obligations | 7 named Claim 5 theorems compiled |
| Build | return code `0`; no `sorryAx` |
| Reported axioms | `propext`, `Classical.choice`, `Quot.sound` only |
| Strict-margin control | rejected, unsolved `False` |
| Sign control | rejected, unsolved `False` |
| Independent finite-domain corroboration | complete four-point envelope error `0.0` |

- Fixed command: `uv run --frozen python run_reproduction.py`
- Git SHA: `3820f7a5601f0d4e52d1936ce045303796519f8d`
- Compute estimate: one active core, uncertain runtime → HF `cpu-upgrade`
- Allocation/runtime: 64 logical CPUs visible, `LAKE_JOBS=1`, 164.07 seconds
- [Exact HF Job](https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f)

## Downloadable code and evidence

[Formal result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/formal_verification_output.json),
[contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/raw_results.json),
[independent checker output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/independent_checker_output.json),
[negative-control output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/negative_control_output.json),
[claim verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/verify.py),
[Lean theorem source](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/LipschitzTransformerFormal/RestrictedStoneWeierstrass.lean),
[product deduction source](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/LipschitzTransformerFormal/TransformerUniversalApproximation.lean),
[formal runner](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/formal_verifier.py),
[failing controls](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/tree/main/formal_negative_controls),
[environment lock](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/uv.lock).

## Limitation

This is an existential density theorem. Compactness supplies finite subcovers
without a constructive cover size, network width/depth, approximation rate, or
training algorithm. Those quantities are not claimed by Lemma 9.
