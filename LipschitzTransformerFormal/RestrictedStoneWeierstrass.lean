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

#print axioms targetRelativeLatticeApproximation

end LipschitzTransformerFormal
