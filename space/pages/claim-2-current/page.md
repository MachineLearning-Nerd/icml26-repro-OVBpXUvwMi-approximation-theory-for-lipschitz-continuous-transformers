# Claim 2 — shallow attention

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact contract

For compact `Omega` and fixed `theta=(A,eta)`, with
`0 <= eta <= 2/sup_y||Ay||^2`, the attention map is 1-Lipschitz in every query
pair for fixed context, and has a finite `W1` Lipschitz constant in every
measure pair for fixed query.

The log-partition Hessian is a tilted covariance, so it is PSD and bounded by
`beta I`. Cocoercivity proves query nonexpansiveness. Compactness bounds the
softmax denominator away from zero; Kantorovich--Rubinstein bounds its
numerator and denominator changes, yielding an explicit finite quotient
constant.

The short lemma wording says the constant depends on `Omega`; its appendix
bound also depends on the fixed `A,eta`. The reproduction tests that precise
fixed-parameter statement. A separate analytic boundary gives ratios
`2,20,200,2000` as `A=s` tends to zero with `eta=2/s^2`, disproving a stronger
uniform-over-parameters reading without contradicting the exact fixed-theta
claim.

## Evidence

- Independent checker: `d=32`, 512 tokens; covariance eigenvalues
  `[1.1355805061e-06, 0.1179650713]`, below beta `1.8345056015`.
- Falsification audit: 1,000 admissible fixed-theta trials; max query Jacobian
  `0.9999999932787749`; no counterexample.
- Negative control: oversized step computes Jacobian norm `1.1`.
- Command/SHA/compute: same fixed command, SHA, and 1.269538-second one-thread
  suite shown on Current verification.

[Contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/raw_results.json),
[independent output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/independent_checker_output.json),
[control](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/negative_control_output.json),
[verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_2/verify.py).

Limitation: no uniform parameter-independent context constant is claimed.
