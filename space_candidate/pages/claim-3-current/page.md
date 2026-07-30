# Claim 3 — finite-depth composition

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact contract

For every finite depth and admissible paper Transformer, the query map is
1-Lipschitz for fixed context and the context map has a finite `W1` Lipschitz
constant for fixed query. The exact Lemma 6 permits the context constant to
depend on both `Omega` and depth `L`.

If layer `l` has query/context constants `q_l<=1,c_l<inf`, the pushforward and
output recurrences are
`r_l <= (q_l+c_l)r_(l-1)` and
`s_l <= q_l s_(l-1)+c_l r_(l-1)`. Induction is finite at every finite depth,
while the fixed-context query product is `prod q_l <= 1`.

## Evidence

- Independent 128-layer recurrence: query product `1.0`; finite context bound
  `3.858201434572288e17`.
- Falsification audit through depth 128: max random query product
  `0.996023516607951`; context recurrence reached `614086.8157`.
- Negative control: insert one layer with constant `1.01`; computed composition
  bound `1.01`, rejected.
- Fixed command: `uv run --frozen python run_reproduction.py`; evidence SHA
  `93baf87fa5bc1c062e83ad36604203d87ba911e4`.

[Contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/raw_results.json),
[independent output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/independent_checker_output.json),
[control](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/negative_control_output.json),
[verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_3/verify.py).

Limitation: “stability does not degrade with depth” applies to the query
constant, not the potentially large context constant.
