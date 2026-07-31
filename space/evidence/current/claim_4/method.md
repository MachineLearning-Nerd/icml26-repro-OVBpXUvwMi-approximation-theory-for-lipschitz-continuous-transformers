# Method

Formalize the arbitrary compact-domain deduction in Lean 4 rather than fitting
a selected target. The kernel checks the product Lipschitz budget, sign-safe
two-point interpolation, restricted Stone–Weierstrass application, and the
scalar ResNet density deduction from its lattice/interpolation obligations.
The executable proof DAG separately audits the architecture-specific lattice,
KR witness, measure integration, and separation chain.

The independent finite-domain envelope is a complete-domain sanity check. The
negative control removes lattice closure: affine functions still separate
points but cannot uniformly approximate `abs(x)` arbitrarily well.

Exact command: `uv run --frozen python run_reproduction.py`.
Primary dependency: Murari et al., arXiv:2505.12003, SHA-256 of the retrieved
alphaXiv full text
`d99938557a22baaae6a470ce281cb850cb568c7249dded51f9a2d6a91b699131`.

Formal run:
`https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f`.
