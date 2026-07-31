# Claim 4 source audit

- Anchor: Theorem `thm:main-approximation`, source lines 492–498.
- Domain: all probability measures on compact `Omega`, not empirical measures
  with a fixed token count. Token-count independence is therefore definitional.
- Dependencies audited: two-variable restricted Stone–Weierstrass; lattice
  closure via parallel attention; KR separation; and Murari et al. (2025),
  Theorem 3.1 for scalar 1-Lipschitz ResNets.
- Singleton `Omega` is handled separately as a constant-domain case because the
  abstract lattice lemma assumes at least two points.
