# Method

The log-partition gradient is the tilted mean of `Ay`; its Hessian is the
tilted covariance. That covariance is PSD and bounded above by
`beta I`, where `beta=sup_y ||Ay||^2`. Cocoercivity of a convex
beta-smooth gradient proves nonexpansiveness for `eta in [0,2/beta]`.

For measure stability, separately bound the numerator and denominator of the
softmax expectation with Kantorovich–Rubinstein duality. Compactness supplies a
positive denominator lower bound, giving an explicit finite quotient bound.

The independent checker uses `d=32`, 512 tokens and direct covariance
eigenvalues. The oversized-step control is rejected.

Exact command: `uv run --frozen python run_reproduction.py`.
