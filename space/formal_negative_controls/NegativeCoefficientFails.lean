import LipschitzTransformerFormal.TransformerUniversalApproximation

-- This is the `[0,1]` claim printed in Lemma 12 for the case `a < b`.
-- Lean must reject it: the valid invariant is `|α| ≤ 1`.
example : 0 ≤ ((-1 : ℝ) - 1) / (1 - 0) := by
  norm_num
