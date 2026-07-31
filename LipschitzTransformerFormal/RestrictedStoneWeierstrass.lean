import Mathlib.Topology.ContinuousMap.StoneWeierstrass

open scoped Topology

namespace LipschitzTransformerFormal

open Set

/--
Target-relative lattice approximation on an arbitrary compact space.

Unlike the usual Stone--Weierstrass theorem, this theorem does not assume that
`L` interpolates arbitrary values.  It only assumes exact two-point
interpolation of the particular target.  This is the compactness argument used
in Lemma 9 of arXiv:2602.15503.
-/
theorem targetRelativeLatticeApproximation
    {X : Type*} [TopologicalSpace X] [CompactSpace X]
    (L : Set C(X, ℝ)) (nL : L.Nonempty)
    (inf_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊓ g ∈ L)
    (sup_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊔ g ∈ L)
    (target : C(X, ℝ))
    (interpolate :
      ∀ x y : X, ∃ g ∈ L, g x = target x ∧ g y = target y)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ L, dist g target < ε := by
  by_cases nX : Nonempty X
  swap
  · exact
      ⟨nL.some, nL.choose_spec,
        (ContinuousMap.dist_lt_iff ε_pos).mpr fun x => False.elim (nX ⟨x⟩)⟩
  choose g hg g_at_x g_at_y using interpolate
  let U : X → X → Set X := fun x y => {z | target z - ε < g x y z}
  have U_nhds_y : ∀ x y, U x y ∈ 𝓝 y := by
    intro x y
    refine IsOpen.mem_nhds ?_ ?_
    · apply isOpen_lt <;> fun_prop
    · rw [Set.mem_setOf_eq, g_at_y]
      exact sub_lt_self _ ε_pos
  let ys : X → Finset X :=
    fun x => (CompactSpace.elim_nhds_subcover (U x) (U_nhds_y x)).choose
  let ys_cover : ∀ x, ⋃ y ∈ ys x, U x y = ⊤ :=
    fun x => (CompactSpace.elim_nhds_subcover (U x) (U_nhds_y x)).choose_spec
  have ys_nonempty : ∀ x, (ys x).Nonempty := fun x =>
    Set.nonempty_of_union_eq_top_of_nonempty _ _ nX (ys_cover x)
  let upper : X → L := fun x =>
    ⟨(ys x).sup' (ys_nonempty x) fun y => (g x y : C(X, ℝ)),
      Finset.sup'_mem _ sup_mem _ _ _ fun y _ => hg x y⟩
  have lower_bound : ∀ x z, target z - ε < (upper x : X → ℝ) z := by
    intro x z
    obtain ⟨y, y_mem, z_mem⟩ :=
      Set.exists_set_mem_of_union_eq_top _ _ (ys_cover x) z
    dsimp [upper]
    simp only [ContinuousMap.coe_sup', Finset.sup'_apply, Finset.lt_sup'_iff]
    exact ⟨y, y_mem, z_mem⟩
  have upper_at_x : ∀ x, (upper x : X → ℝ) x = target x := by
    intro x
    simp [upper, g_at_x]
  let W : X → Set X := fun x => {z | (upper x : X → ℝ) z < target z + ε}
  have W_nhds : ∀ x, W x ∈ 𝓝 x := by
    intro x
    refine IsOpen.mem_nhds ?_ ?_
    · apply isOpen_lt <;> fun_prop
    · dsimp only [W, Set.mem_setOf_eq]
      rw [upper_at_x]
      exact lt_add_of_pos_right _ ε_pos
  let xs : Finset X := (CompactSpace.elim_nhds_subcover W W_nhds).choose
  let xs_cover : ⋃ x ∈ xs, W x = ⊤ :=
    (CompactSpace.elim_nhds_subcover W W_nhds).choose_spec
  have xs_nonempty : xs.Nonempty :=
    Set.nonempty_of_union_eq_top_of_nonempty _ _ nX xs_cover
  let approximant : L :=
    ⟨xs.inf' xs_nonempty fun x => (upper x : C(X, ℝ)),
      Finset.inf'_mem _ inf_mem _ _ _ fun x _ => (upper x).2⟩
  refine ⟨approximant.1, approximant.2, ?_⟩
  rw [ContinuousMap.dist_lt_iff ε_pos]
  intro z
  rw [show ∀ a b δ : ℝ, dist a b < δ ↔ a < b + δ ∧ b - δ < a by
    intros
    simp only [← Metric.mem_ball, Real.ball_eq_Ioo, Set.mem_Ioo, and_comm]]
  constructor
  · simp only [approximant, Finset.inf'_lt_iff, ContinuousMap.inf'_apply]
    exact Set.exists_set_mem_of_union_eq_top _ _ xs_cover z
  · simp only [approximant, Finset.lt_inf'_iff, ContinuousMap.inf'_apply]
    intro x _
    exact lower_bound x z

/-- Every continuous target has a strict positive scaling arbitrarily close in
uniform distance.  This is the strict-margin device in Lemma 9. -/
theorem existsStrictScaleNear
    {X : Type*} [TopologicalSpace X] [CompactSpace X]
    (target : C(X, ℝ)) {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ ρ : ℝ, 0 < ρ ∧ ρ < 1 ∧ dist (ρ • target) target < ε := by
  let denominator : ℝ := 2 * (ε + ‖target‖ + 1)
  have denominator_pos : 0 < denominator := by
    dsimp [denominator]
    positivity
  let t : ℝ := ε / denominator
  have t_pos : 0 < t := div_pos ε_pos denominator_pos
  have t_lt_one : t < 1 := by
    apply (div_lt_one denominator_pos).2
    dsimp [denominator]
    nlinarith [norm_nonneg target]
  let ρ : ℝ := 1 - t
  have ρ_pos : 0 < ρ := by dsimp [ρ]; linarith
  have ρ_lt_one : ρ < 1 := by dsimp [ρ]; linarith
  have t_norm_lt : t * ‖target‖ < ε := by
    dsimp [t]
    rw [div_mul_eq_mul_div]
    apply (div_lt_iff₀ denominator_pos).2
    dsimp [denominator]
    nlinarith [norm_nonneg target]
  refine ⟨ρ, ρ_pos, ρ_lt_one, ?_⟩
  apply (ContinuousMap.dist_lt_iff ε_pos).2
  intro x
  have apply_norm : |target x| ≤ ‖target‖ := by
    simpa [Real.norm_eq_abs] using target.norm_coe_le_norm x
  calc
    dist ((ρ • target) x) (target x) =
        |(ρ - 1) * target x| := by
          rw [Real.dist_eq, ContinuousMap.smul_apply, smul_eq_mul]
          congr 1
          ring
    _ = t * |target x| := by
      rw [abs_mul]
      simp [ρ, abs_of_pos t_pos]
    _ ≤ t * ‖target‖ :=
      mul_le_mul_of_nonneg_left apply_norm t_pos.le
    _ < ε := t_norm_lt

/--
Restricted lattice density once every strict scaling of the target admits
two-point interpolants.  Both quantifiers are universal: no finite sample or
chosen basis appears.
-/
theorem restrictedLatticeApproximationOfScaledInterpolation
    {X : Type*} [TopologicalSpace X] [CompactSpace X]
    (L : Set C(X, ℝ)) (nL : L.Nonempty)
    (inf_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊓ g ∈ L)
    (sup_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊔ g ∈ L)
    (target : C(X, ℝ))
    (scaled_interpolate :
      ∀ (ρ : ℝ), 0 < ρ → ρ < 1 → ∀ x y : X,
        ∃ g ∈ L, g x = (ρ • target) x ∧ g y = (ρ • target) y)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ L, dist g target < ε := by
  have half_pos : 0 < ε / 2 := by positivity
  obtain ⟨ρ, ρ_pos, ρ_lt_one, scale_close⟩ :=
    existsStrictScaleNear target half_pos
  obtain ⟨g, g_mem, g_close⟩ :=
    targetRelativeLatticeApproximation L nL inf_mem sup_mem (ρ • target)
      (scaled_interpolate ρ ρ_pos ρ_lt_one) half_pos
  refine ⟨g, g_mem, ?_⟩
  calc
    dist g target ≤ dist g (ρ • target) + dist (ρ • target) target :=
      dist_triangle _ _ _
    _ < ε := by linarith

/-- Strict scaling turns a non-strict budget-Lipschitz inequality into a
strict one at every pair of distinct points. -/
theorem strictGapOfScale
    {X : Type*} [TopologicalSpace X]
    (budget : X → X → ℝ)
    (budget_pos : ∀ x y, x ≠ y → 0 < budget x y)
    (target : C(X, ℝ))
    (target_lipschitz :
      ∀ x y, |target x - target y| ≤ budget x y)
    {ρ : ℝ} (ρ_pos : 0 < ρ) (ρ_lt_one : ρ < 1)
    {x y : X} (xy_ne : x ≠ y) :
    |(ρ • target) x - (ρ • target) y| < budget x y := by
  rw [ContinuousMap.smul_apply, ContinuousMap.smul_apply, smul_eq_mul,
    smul_eq_mul, ← mul_sub, abs_mul, abs_of_pos ρ_pos]
  calc
    ρ * |target x - target y| ≤ ρ * budget x y :=
      mul_le_mul_of_nonneg_left (target_lipschitz x y) ρ_pos.le
    _ < 1 * budget x y :=
      mul_lt_mul_of_pos_right ρ_lt_one (budget_pos x y xy_ne)
    _ = budget x y := one_mul _

/--
The exact restricted Stone--Weierstrass contract used by Lemma 9, expressed
for an arbitrary positive pair budget.  The product Wasserstein/query budget
is instantiated below.
-/
theorem restrictedStoneWeierstrass
    {X : Type*} [TopologicalSpace X] [CompactSpace X] [Nontrivial X]
    (budget : X → X → ℝ)
    (budget_pos : ∀ x y, x ≠ y → 0 < budget x y)
    (L : Set C(X, ℝ)) (nL : L.Nonempty)
    (inf_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊓ g ∈ L)
    (sup_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊔ g ∈ L)
    (strict_interpolate :
      ∀ x y : X, x ≠ y → ∀ a b : ℝ, |a - b| < budget x y →
        ∃ g ∈ L, g x = a ∧ g y = b)
    (target : C(X, ℝ))
    (target_lipschitz :
      ∀ x y, |target x - target y| ≤ budget x y)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ L, dist g target < ε := by
  apply
    restrictedLatticeApproximationOfScaledInterpolation
      L nL inf_mem sup_mem target _ ε_pos
  intro ρ ρ_pos ρ_lt_one x y
  by_cases xy : x = y
  · subst y
    obtain ⟨z, xz⟩ := exists_ne x
    have x_ne_z : x ≠ z := Ne.symm xz
    obtain ⟨g, g_mem, g_at_x, _⟩ :=
      strict_interpolate x z x_ne_z ((ρ • target) x) ((ρ • target) z)
        (strictGapOfScale budget budget_pos target target_lipschitz
          ρ_pos ρ_lt_one x_ne_z)
    exact ⟨g, g_mem, g_at_x, g_at_x⟩
  · exact
      strict_interpolate x y xy ((ρ • target) x) ((ρ • target) y)
        (strictGapOfScale budget budget_pos target target_lipschitz
          ρ_pos ρ_lt_one xy)

/-- The paper's two-variable Lipschitz budget. -/
def productBudget
    {U V : Type*} [MetricSpace U] [MetricSpace V]
    (C : ℝ) (p q : U × V) : ℝ :=
  dist p.2 q.2 + C * dist p.1 q.1

theorem productBudget_pos
    {U V : Type*} [MetricSpace U] [MetricSpace V]
    {C : ℝ} (C_pos : 0 < C) {p q : U × V} (pq_ne : p ≠ q) :
    0 < productBudget C p q := by
  by_cases first_eq : p.1 = q.1
  · have second_ne : p.2 ≠ q.2 := by
      intro second_eq
      exact pq_ne (Prod.ext first_eq second_eq)
    have second_pos : 0 < dist p.2 q.2 := dist_pos.mpr second_ne
    have first_nonneg : 0 ≤ dist p.1 q.1 := dist_nonneg
    dsimp [productBudget]
    nlinarith
  · have first_pos : 0 < dist p.1 q.1 := dist_pos.mpr first_eq
    have second_nonneg : 0 ≤ dist p.2 q.2 := dist_nonneg
    dsimp [productBudget]
    nlinarith

/--
Lemma 9 specialized to compact metric `U × V` and the paper's
`dist_V + C * dist_U` budget.
-/
theorem restrictedStoneWeierstrassProduct
    {U V : Type*} [MetricSpace U] [MetricSpace V]
    [CompactSpace U] [CompactSpace V] [Nontrivial (U × V)]
    {C : ℝ} (C_pos : 0 < C)
    (L : Set C(U × V, ℝ)) (nL : L.Nonempty)
    (inf_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊓ g ∈ L)
    (sup_mem : ∀ f ∈ L, ∀ g ∈ L, f ⊔ g ∈ L)
    (strict_interpolate :
      ∀ p q : U × V, p ≠ q → ∀ a b : ℝ,
        |a - b| < productBudget C p q →
        ∃ g ∈ L, g p = a ∧ g q = b)
    (target : C(U × V, ℝ))
    (target_lipschitz :
      ∀ p q, |target p - target q| ≤ productBudget C p q)
    {ε : ℝ} (ε_pos : 0 < ε) :
    ∃ g ∈ L, dist g target < ε :=
  restrictedStoneWeierstrass (productBudget C)
    (fun _ _ h => productBudget_pos C_pos h) L nL inf_mem sup_mem
    strict_interpolate target target_lipschitz ε_pos

#print axioms targetRelativeLatticeApproximation
#print axioms existsStrictScaleNear
#print axioms restrictedStoneWeierstrass
#print axioms restrictedStoneWeierstrassProduct

end LipschitzTransformerFormal
