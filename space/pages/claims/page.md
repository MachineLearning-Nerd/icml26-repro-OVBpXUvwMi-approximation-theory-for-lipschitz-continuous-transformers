# claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a56661427d0c", "created_at": "2026-07-29T10:05:41+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. **Construction**: the MLP block F_ξ(x)=x−τWᵀσ(Wx+b) and attention block Γ_θ(μ,x)=x−ηA·E[y·softmax⟨x,Ay⟩] are explicit Euler steps of the negative gradient flows −∇g (g=1ᵀγ(Wx+b), γ′=ReLU) and −∇λ (λ=log E exp⟨x,Ay⟩), making the architecture Lipschitz-continuous by construction (Section 3).
2. **Lemma 2**: Γ_θ(μ,·) is 1-Lipschitz in the query x for η∈[0, 2/sup_y‖Ay‖²], and Γ_θ(·,x) is C₁-Lipschitz in the context measure μ under W₁.
3. **Lemma 6**: a deep Transformer T(μ,·) is 1-Lipschitz in the query (composition of non-expansive blocks), independent of depth.
4. **Theorem 8**: the scalar-Lipschitz-Transformer class G_C universally approximates any 1-Lipschitz in-context map Λ* within ε (via the Restricted Stone-Weierstrass theorem).
5. **Lemma 9**: Restricted Stone-Weierstrass for 2-variable Lipschitz functions — a subalgebra of C(U×X) that separates points and is 1-Lipschitz in x for each u is dense.
