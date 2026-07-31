# Claim 1 source audit

- Source: arXiv source archive `2602.15503`, SHA-256
  `d7d496f38d43b90a9056463183dd7368c4e620af49324a8b16f43f5d67dc80a2`.
- Anchor: “Lipschitz MLP layer,” equation `eq:1lipMLP`, Lemma
  `lem:MLP-Lip` (source lines 203–213).
- Exact scope: all dimensions, widths, matrices, biases and inputs, with ReLU
  and the stated closed step interval. This is not a finite-scale claim.
- Edge case: `W=0` is the identity map; the reciprocal endpoint is interpreted
  separately rather than dividing by zero.
