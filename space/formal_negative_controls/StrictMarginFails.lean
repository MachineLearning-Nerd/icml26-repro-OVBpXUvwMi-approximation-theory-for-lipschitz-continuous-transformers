import LipschitzTransformerFormal.RestrictedStoneWeierstrass

-- A metric-saturating target does not satisfy the strict interpolation
-- premise before scaling.  Lean must reject this proposition.
example : |(0 : ℝ) - 1| < |(0 : ℝ) - 1| := by
  norm_num
