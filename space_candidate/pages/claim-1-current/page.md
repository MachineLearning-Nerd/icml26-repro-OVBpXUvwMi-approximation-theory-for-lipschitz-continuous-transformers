# Claim 1 — MLP Euler layer

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact contract

For every `d,k`, every real `W,b`, and all input pairs, with ReLU and
`0 <= tau <= 2/||W||_2^2`,
`F(x)=x-tau W^T ReLU(Wx+b)` is both the explicit negative-gradient Euler step
and 1-Lipschitz. `W=0` is the identity edge case.

On every activation segment,
`J=I-tau W^T D W`, where `0<=D<=I`. Hence
`0<=W^T D W<=||W||_2^2 I`, so every Jacobian eigenvalue is in `[-1,1]`.
Continuity across the finitely many segment crossings gives the global bound.

## Evidence

- Certificate: Claim 1 node and all three dependencies passed.
- Independent checker: `d=16`, width 10, all 1,024 activation masks;
  maximum operator norm `1.0000000000000009` (roundoff tolerance `5e-12`).
- Negative control: `tau=2.1/||W||^2` computes Lipschitz constant `1.1` and is
  rejected.
- Fixed command: `uv run --frozen python run_reproduction.py`
- SHA `488295b34cfd0b7e7f0ad2c1cbded67370fa4d9a`; seeds `101` plus campaign seeds
- Local one-thread CPU; 8 logical CPUs visible; whole suite 1.805414 seconds.

[Contract](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/source_audit.md),
[raw result](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/raw_results.json),
[independent output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/independent_checker_output.json),
[control output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/negative_control_output.json),
[verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/claim_1/verify.py).

Limitation: the numerical exhaustion is finite corroboration only; the
dimension-free spectral derivation is the verification.
