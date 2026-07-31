# Method

For fixed input measure, propagated measures are fixed with respect to the query,
so query constants multiply and remain at most one. For contexts, use
`W1(f_mu#mu, f_nu#nu) <= Lip_x(f_mu) W1(mu,nu) +
sup_y||f_mu(y)-f_nu(y)||`; this gives a finite recurrence through every finite
layer sequence. The independent checker evaluates the recurrence for 128 layers.
An inserted 1.01-Lipschitz layer is the required failing control.

Exact command: `uv run --frozen python run_reproduction.py`.
