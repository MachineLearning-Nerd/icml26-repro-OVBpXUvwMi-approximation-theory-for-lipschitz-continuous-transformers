# Claim 4 — universal approximation

**Verdict: VERIFIED. Confidence: MEDIUM.**

## Exact contract

For every compact `Omega` in every finite dimension, every `C>0`, every target
that is 1-Lipschitz in the query and C-Lipschitz in `W1` context, and every
`epsilon in (0,1)`, there exists a paper-class scalar Transformer with uniform
error at most epsilon. The domain is all probability measures, so the
guarantee is not tied to a token count.

This is not tested by fitting a convenient target. The reconstruction verifies:

1. lattice closure by parallel attention/MLP construction and an exact ReLU
   max/min identity;
2. a compact-domain Kantorovich--Rubinstein optimizer;
3. scalar Lipschitz ResNet approximation of that arbitrary witness;
4. uniform-score attention realizing its context integral;
5. strict product-metric point separation; and
6. the independently reconstructed Claim 5 density lemma.

The final interpolation scale has absolute value at most one; negative signs
are handled by the linear projection. Singleton and zero-witness edge cases
are handled separately.

## Evidence

- Certificate: all 25 nodes passed; zero errors.
- Complete four-point finite domain: lattice envelope error `0.0`; Dirac
  `W1=1.2884098726725126`, exactly matched by the KR witness.
- Negative control: affine functions separate points but are not a lattice;
  their uniform error for `abs(x)` is at least `0.5`.
- Fixed command/SHA/runtime: same as Current verification.

[Contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/raw_results.json),
[control](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/negative_control_output.json),
[proof derivation](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/symbolic_derivation.md),
[verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_4/verify.py).

## Limitation

Remaining risk: the chain imports Murari et al., Theorem 3.1. Its source was
audited (arXiv:2505.12003, retrieved full-text SHA
`d99938557a22baaae6a470ce281cb850cb568c7249dded51f9a2d6a91b699131`)
but was not proof-assistant formalized. That material risk keeps confidence
MEDIUM.
