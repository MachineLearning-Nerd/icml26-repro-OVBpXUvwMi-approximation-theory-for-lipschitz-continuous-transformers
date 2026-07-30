# Claim 5 — restricted Stone-Weierstrass

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact contract

On compact metric spaces `U,X`, any lattice `L` inside the separately
`(1,C)`-Lipschitz functions is uniformly dense if it can interpolate every
two-point value pair whose gap is strictly below
`d_X(x,y)+C d_U(u,v)`.

For an arbitrary target, scale by
`rho=1-epsilon/(2(1+||g||_inf))`. This creates the strict margin while costing
at most epsilon/2. Separation supplies local interpolants. A compact finite
subcover plus lattice minimum makes global upper envelopes; a second compact
subcover plus lattice maximum sandwiches the scaled target within epsilon/2.
No target-derived basis is used.

Kantorovich--Rubinstein duality is used later to verify separation for the
Transformer class; it is not an assumption of this abstract lemma.

## Evidence

- Certificate: strict scaling, interpolants, min cover, max cover, and final
  density nodes all passed.
- Complete finite-domain envelope error `0.0`; separate 400-case audit maximum
  `4.440892098500626e-16`.
- Negative control: omit scaling for a metric-saturating target; computed gap
  equals distance, so the required strict premise is false and rejected.
- Fixed command/SHA/runtime: same as Current verification.

[Contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/raw_results.json),
[control](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/negative_control_output.json),
[proof derivation](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/symbolic_derivation.md),
[verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_5/verify.py).

Limitation: this is a mathematical existence/density result, not a complexity
or trainability guarantee.
