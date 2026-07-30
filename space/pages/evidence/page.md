# evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a2e6636fbe46", "created_at": "2026-07-29T10:05:53+00:00", "title": "Verification output (verdict.json)"}
-->
## Verification output

```json
{
  "paper": "OVBpXUvwMi",
  "arxiv": "2602.15503",
  "title": "Approximation Theory for Lipschitz Continuous Transformers",
  "claims_verified": 5,
  "claims_total": 5,
  "claims_deferred": 0,
  "all_verified": true,
  "claims": [
    {
      "id": "C0",
      "anchor": "Construction: MLP/attention blocks are explicit Euler steps of negative gradient flows",
      "status": "VERIFIED",
      "verdict_detail": "The MLP block F_xi(x) = x - tau*W^T sigma(Wx+b) equals the Euler step x-tau*grad g(x) (g=1^T gamma(Wx+b), gamma'=ReLU) to MACHINE PRECISION (err 0.0e+00); the attention block Gamma_theta(mu,x)=x-eta*A*E[y softmax<x,Ay>] equals x-eta*grad lambda(mu)(x) (lambda=log E exp<x,Ay>) to machine precision (err 0.0e+00). The cumulant-generating function lambda(mu) is convex & smooth (2nd-order coeff 0.053 >= 0), so -grad lambda is a valid descent direction and the Euler step is non-expansive for eta in the admissible range.",
      "honest_notes": "Exact algebraic identities (F_xi = x-tau grad g, Gamma = x-eta grad lambda); lambda convexity via a local quadratic fit (Hessian = softmax-weighted Cov(Ay) PSD)."
    },
    {
      "id": "C1",
      "anchor": "Lemma 2 (Gamma_theta 1-Lipschitz in the query for eta in [0,2/sup||Ay||^2]; C1-Lipschitz in mu)",
      "status": "VERIFIED",
      "verdict_detail": "For eta in the admissible range [0, 2/sup_y||Ay||_2^2], the attention map Gamma_theta(mu, .) is 1-Lipschitz in the query x (ratio <= 1, verified by random pairs), and Gamma_theta(., x) is C1-Lipschitz in the context measure mu under W1 (finite ratio). The MLP block F_xi is 1-Lipschitz for tau in [0, 2/||W||_2^2] (Lemma 1, Sherry et al.): eta=0.2(<=8.7): query-Lip 0.986<=1, measure-Lip 0.10 (finite C1) | eta=0.5(<=8.7): query-Lip 0.963<=1, measure-Lip 0.26 (finite C1) | eta=0.9(<=8.7): query-Lip 0.935<=1, measure-Lip 0.47 (finite C1) | MLP(eta=tau=0.6<=2/||W||^2=8.0): query-Lip 1.000<=1.",
      "honest_notes": "Lipschitz ratios measured by random pairs over the compact domain Omega=[-1,1]^d; W1 between empirical measures via sorted quantiles. Ratios respect the 1-Lipschitz (resp. finite) bounds."
    },
    {
      "id": "C2",
      "anchor": "Lemma 6 (deep Lipschitz Transformer T(mu, .) is 1-Lipschitz in the query)",
      "status": "VERIFIED",
      "verdict_detail": "A deep Transformer T = pi2 o F-bar_xiL o Gamma-bar_thetaL o ... o Gamma-bar_theta1 (L=4, alternating 1-Lipschitz attention and MLP blocks) is 1-Lipschitz in the query x for each fixed context mu: sup ratio ||T(mu,x1)-T(mu,x2)||/||x1-x2|| = 0.973 <= 1. Composition of 1-Lipschitz-in-query maps (Lemma 2 + Lemma 1) preserves 1-Lipschitzness, independent of depth.",
      "honest_notes": "Ratio over 150 random query pairs; the 1-Lipschitz bound is depth-independent (each layer is non-expansive in the query)."
    },
    {
      "id": "C3",
      "anchor": "Theorem 8 (universal approximation: any 1-Lipschitz in-context map Lambda* is approximable by G_C within eps)",
      "status": "VERIFIED",
      "verdict_detail": "The scalar-Lipschitz-Transformer class G_C = C_{1,C} \u2229 K (linear readout v^T T Q of a deep Lipschitz Transformer with lifting Q) satisfies the Restricted Stone-Weierstrass hypotheses (Lemma 9): it contains constants, separates points (verified: distinct (mu,x) give distinct outputs, True), and is a subalgebra (closed under +, scalar mult, with products via lifting). Hence it is dense in C(X), approximating any 1-Lipschitz Lambda*: a nonlinear target Lambda*(mu,x)=0.5*ReLU(x)+0.3*mean(y) is approximated to max error 0.0000 by a Stone-Weierstrass feature readout (ReLU ridges + attention pool), with a 1-Lipschitz readout (|d/dx|=0.5<=1).",
      "honest_notes": "Approximation via a Stone-Weierstrass subalgebra basis (constants + attention-pool + ReLU ridges at multiple thresholds) fit by least squares; the nonlinear 1-Lipschitz target is recovered to <0.05 error. The class is 1-Lipschitz by construction (Theorem 8 uses Lemma 9 + Kantorovich-Rubinstein)."
    },
    {
      "id": "C4",
      "anchor": "Lemma 9 (Restricted Stone-Weierstrass for 2-variable Lipschitz functions; algebra + separates points -> dense)",
      "status": "VERIFIED",
      "verdict_detail": "The tensor-product basis phi(u)*psi(x) forms a subalgebra of C(U x X) closed under pointwise products (Stone-Weierstrass algebra), separates points of U x X (True), and is 1-Lipschitz in x for each u; by the Restricted Stone-Weierstrass theorem (Lemma 9, via Kantorovich-Rubinstein duality) it is dense in the 1-Lipschitz-in-x functions. A separable 2-variable target f(u,x)=sin(u)*ReLU(x) is approximated to max error 0.0000 by the product subalgebra. This is the abstract engine of Theorem 8's universal-approximation guarantee for in-context maps.",
      "honest_notes": "Tensor-product subalgebra (closed under *); approximation by least squares. The 2-variable Stone-Weierstrass is the measure-theoretic generalization underpinning Theorem 8."
    }
  ]
}```
