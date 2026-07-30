# Method

Scale any target toward zero to turn non-strict Lipschitz inequalities into the
strict separation premise. At each fixed point, use separation and compactness
to take a finite minimum giving a global upper envelope. A second compact cover
and finite maximum gives the lower envelope. The two envelopes sandwich the
scaled target uniformly; scaling error completes the proof.

The control omits scaling for a metric-saturating target, so the strict
precondition is false and the proof kernel rejects the route.

Exact command: `uv run --frozen python run_reproduction.py`.
