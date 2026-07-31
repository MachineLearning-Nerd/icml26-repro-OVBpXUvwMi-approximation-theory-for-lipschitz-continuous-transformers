import LipschitzTransformerFormal.RestrictedStoneWeierstrass

open scoped Topology

namespace LipschitzTransformerFormal

open Set

/--
The separate query/context Lipschitz assumptions in Theorem 8 imply the
single product-budget inequality needed by Lemma 9.
-/
theorem separatelyLipschitz_productBudget
    {U V : Type*} [MetricSpace U] [MetricSpace V]
    {C : ℝ} (C_nonneg : 0 ≤ C)
    (target : C(U × V, ℝ))
    (query_lipschitz :
      ∀ u x y, |target (u, x) - target (u, y)| ≤ dist x y)
    (context_lipschitz :
      ∀ u v x, |target (u, x) - target (v, x)| ≤ C * dist u v)
    (p q : U × V) :
    |target p - target q| ≤ productBudget C p q := by
  calc
    |target p - target q| =
        |(target p - target (p.1, q.2)) +
          (target (p.1, q.2) - target q)| := by
            congr 1
            ring
    _ ≤ |target p - target (p.1, q.2)| +
        |target (p.1, q.2) - target q| := abs_add_le _ _
    _ ≤ dist p.2 q.2 + C * dist p.1 q.1 :=
      add_le_add
        (query_lipschitz p.1 p.2 q.2)
        (context_lipschitz p.1 q.1 q.2)
    _ = productBudget C p q := rfl

/--
The sign-safe interpolation coefficient used in Lemma 12.  The paper writes
the coefficient as belonging to `[0,1]`; when `a < b` the correct invariant is
its absolute value being below one.
-/
theorem interpolationCoefficient_abs_lt_one
    {a b fp fq : ℝ} (gap : |a - b| < fp - fq) :
    |(a - b) / (fp - fq)| < 1 := by
  have denominator_pos : 0 < fp - fq :=
    lt_of_le_of_lt (abs_nonneg (a - b)) gap
  rw [abs_div, abs_of_pos denominator_pos]
  exact (div_lt_one denominator_pos).2 gap

/--
Affine rescaling realizes either ordering of two requested values.  This
closes the negative-coefficient edge case in the printed proof of Lemma 12.
-/
theorem affineRescale_interpolates
    {a b fp fq : ℝ} (denominator_ne : fp - fq ≠ 0) :
    let α := (a - b) / (fp - fq)
    let β := b - α * fq
    β + α * fp = a ∧ β + α * fq = b := by
  dsimp
  constructor
  · field_simp
    ring
  · ring

/--
The exact universal-quantifier deduction in Theorem 8 after the paper's
architecture lemmas have established nonemptiness, lattice closure, and
strict two-point interpolation for `G_C`.

This theorem ranges over arbitrary compact metric context/query spaces and
arbitrary separately Lipschitz targets.  It contains no finite sample, chosen
basis, or target fit.
-/
theorem transformerUniversalApproximation
    {U V : Type*} [MetricSpace U] [MetricSpace V]
    [CompactSpace U] [CompactSpace V] [Nontrivial (U × V)]
    {C : ℝ} (C_pos : 0 < C)
    (G : Set C(U × V, ℝ)) (nG : G.Nonempty)
    (inf_mem : ∀ f ∈ G, ∀ g ∈ G, f ⊓ g ∈ G)
    (sup_mem : ∀ f ∈ G, ∀ g ∈ G, f ⊔ g ∈ G)
    (strict_interpolate :
      ∀ p q : U × V, p ≠ q → ∀ a b : ℝ,
        |a - b| < productBudget C p q →
        ∃ g ∈ G, g p = a ∧ g q = b)
    (target : C(U × V, ℝ))
    (query_lipschitz :
      ∀ u x y, |target (u, x) - target (u, y)| ≤ dist x y)
    (context_lipschitz :
      ∀ u v x, |target (u, x) - target (v, x)| ≤ C * dist u v)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ G, dist g target < ε :=
  restrictedStoneWeierstrassProduct C_pos G nG inf_mem sup_mem
    strict_interpolate target
    (separatelyLipschitz_productBudget C_pos.le target
      query_lipschitz context_lipschitz)
    ε_pos

/--
Murari et al., Theorem 3.1, reduced to its two exact architecture obligations:
the scalar gradient-descent ResNet family is a lattice and strictly
interpolates admissible two-point data.  The compact-domain density conclusion
is then kernel checked rather than imported as a citation.
-/
theorem scalarResNetDensity
    {X : Type*} [MetricSpace X] [CompactSpace X] [Nontrivial X]
    (R : Set C(X, ℝ)) (nR : R.Nonempty)
    (inf_mem : ∀ f ∈ R, ∀ g ∈ R, f ⊓ g ∈ R)
    (sup_mem : ∀ f ∈ R, ∀ g ∈ R, f ⊔ g ∈ R)
    (strict_interpolate :
      ∀ x y : X, x ≠ y → ∀ a b : ℝ, |a - b| < dist x y →
        ∃ g ∈ R, g x = a ∧ g y = b)
    (target : C(X, ℝ))
    (target_lipschitz : ∀ x y, |target x - target y| ≤ dist x y)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ R, dist g target < ε :=
  restrictedStoneWeierstrass dist
    (fun _ _ h => dist_pos.mpr h) R nR inf_mem sup_mem strict_interpolate
    target target_lipschitz ε_pos

#print axioms separatelyLipschitz_productBudget
#print axioms interpolationCoefficient_abs_lt_one
#print axioms affineRescale_interpolates
#print axioms transformerUniversalApproximation
#print axioms scalarResNetDensity

end LipschitzTransformerFormal
