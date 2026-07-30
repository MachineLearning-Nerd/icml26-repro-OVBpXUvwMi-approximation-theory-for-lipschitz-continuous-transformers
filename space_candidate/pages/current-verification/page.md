# Current verification

**Supersedes:** judged revision
`df0a8cc0348a130d23bce8f00c22eaa00452aa3d`, whose d=1 sampled pages remain
preserved as **Historical rejected baseline**.

The paper's five claims are universally quantified. Finite experiments cannot
prove them. Current verdicts therefore rest on an independently reconstructed
symbolic derivation, with an executable dependency certificate and separate
checks/controls. Numerical results only corroborate the algebra.

| Claim | Exact scope tested | Verdict | Confidence | Strongest independent check | Control |
| --- | --- | --- | --- | --- | --- |
| [1](#/claim-1-current) | Every admissible dimension, matrix, bias, input, and closed step interval | VERIFIED | HIGH | all 1,024 masks at d=16; max norm 1.0000000000000009 | oversized step gives 1.1 |
| [2](#/claim-2-current) | Fixed parameters; every context/query or measure pair on compact Omega | VERIFIED | HIGH | d=32, 512 tokens; covariance max 0.1179650713 <= 1.8345056015 | oversized step gives 1.1 |
| [3](#/claim-3-current) | Every finite depth; query constant <=1; finite depth-dependent context constant | VERIFIED | HIGH | 128 layers; query product 1.0 | one 1.01 layer gives 1.01 |
| [4](#/claim-4-current) | Every target in C_(1,C) and every epsilon in (0,1) | VERIFIED | MEDIUM | full lattice/KR/separation proof chain | removing lattice leaves >=0.5 error |
| [5](#/claim-5-current) | Every target on compact product metric spaces under strict separation | VERIFIED | HIGH | two-cover symbolic proof; complete finite-domain error 0 | omitting scaling violates strict premise |

## Reproduce

```bash
uv run --frozen python run_reproduction.py
```

- Evidence run Git SHA:
  `93baf87fa5bc1c062e83ad36604203d87ba911e4`
- CPython 3.12.11; NumPy 2.5.1; exact `uv.lock`
- Estimated cores: 1; local CPU; numerical libraries limited to one thread
- Visible allocation: 8 logical CPUs; measured runtime: 1.269538 seconds
- Deterministic seeds: `0,1,2,3,5,7,11`; independent checks use `101,202`
- Certificate: 25/25 dependency nodes, zero errors
- Independent checker: all checks passed
- Negative controls: 5/5 rejected for their intended reason

Download:
[raw run evidence](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/release_evidence.json),
[proof DAG](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/proof_dag.json),
[symbolic derivation](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/symbolic_derivation.md),
[entrypoint](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/run_reproduction.py),
[proof verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/proof_verifier.py),
[independent checker](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/independent_checker.py),
[negative controls](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/negative_controls.py),
[environment](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/uv.lock).

## Falsification audit

A separate HF `cpu-upgrade` run used 64 logical CPUs with a one-thread
numerical limit. Estimated need was 2 cores because runtime was uncertain;
provider runtime was 16 seconds and measured audit runtime was 0.249335
seconds. It searched 1,000 admissible Claim 1 instances, 1,000 fixed-parameter
Claim 2 instances, depth through 128, and 400 complete finite metric
instances. No exact-claim counterexample was found. This failed search is not
treated as proof.

It did expose two wording boundaries: Claim 2's context constant cannot be
uniform over all `A,eta`, and Claim 3's context constant can grow with depth.
[Raw falsification output](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/falsification_output.json).

## Limitations

- Claim 4 imports Murari et al., Theorem 3.1; that antecedent was source-audited
  but not proof-assistant formalized. This is why confidence is MEDIUM.
- The executable certificate checks the reconstructed dependency chain; it is
  not a Lean/Coq formalization.
- The finite checks are scale-independent diagnostics, not empirical proof of
  universal quantifiers.
- No practical training, accuracy, or vector-output claim is made by the paper
  or this reproduction.
