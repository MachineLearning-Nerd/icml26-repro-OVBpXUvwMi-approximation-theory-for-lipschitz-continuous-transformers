# Method

Differentiate the convex ReLU potential on every activation segment. The
Jacobian is `I - tau W^T D W`, where `0 <= D <= I`. Therefore
`0 <= W^T D W <= ||W||_2^2 I`; the step bound places every Jacobian eigenvalue
in `[-1,1]`. Continuity across segment boundaries gives the global bound.

The trusted dependency checker verifies this derivation. A separate
implementation exhausts all 1,024 activation masks for a 16-dimensional,
10-unit instance. The control uses `tau=2.1/||W||^2` and must be rejected.

Exact command: `uv run --frozen python run_reproduction.py`.
Environment: CPython 3.12.11 and NumPy 2.5.1 from `uv.lock`.
