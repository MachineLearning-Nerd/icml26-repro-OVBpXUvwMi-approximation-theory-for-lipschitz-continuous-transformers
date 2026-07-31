# Method

Scale any target toward zero to turn non-strict Lipschitz inequalities into the
strict separation premise. At each fixed point, use separation and compactness
to take a finite minimum giving a global upper envelope. A second compact cover
and finite maximum gives the lower envelope. The two envelopes sandwich the
scaled target uniformly; scaling error completes the proof.

The control omits scaling for a metric-saturating target, so the strict
precondition is false and the proof kernel rejects the route.

Exact command: `uv run --frozen python run_reproduction.py`.

Lean 4.19.0 with mathlib v4.19.0 compiles the theorem and prints only the
standard axioms `propext`, `Classical.choice`, and `Quot.sound`. Two deliberately
false theorems are rejected. Formal run:
`https://huggingface.co/jobs/DineshAI/6a6c0f3023ed89c748ec8e1f`.
