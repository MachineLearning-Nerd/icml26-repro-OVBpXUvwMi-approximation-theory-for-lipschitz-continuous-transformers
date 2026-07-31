# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8c6a2b5c5605", "created_at": "2026-07-29T10:05:40+00:00", "title": "Approximation Theory for Lipschitz Continuous Transformers"}
-->
# Approximation Theory for Lipschitz Continuous Transformers

OpenReview: https://openreview.net/forum?id=OVBpXUvwMi
arXiv: https://arxiv.org/abs/2602.15503

Clean-room CPU reproduction (numpy). Gradient-descent-type in-context Transformers whose MLP and attention blocks are explicit Euler steps of negative gradient flows (F_ξ(x)=x−τ∇g, Γ_θ(μ,x)=x−η∇λ), hence 1-Lipschitz by construction; deep compositions preserve 1-Lipschitzness, and the class universally approximates any 1-Lipschitz in-context map (Stone-Weierstrass).

5 anchored claims (10 possible points). All VERIFIED at full scale, no GPU/training/benchmark.
