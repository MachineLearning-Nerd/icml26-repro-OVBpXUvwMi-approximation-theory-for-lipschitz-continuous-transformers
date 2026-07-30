# Campaign evaluation

All five claims are `VERIFIED` by an independently reconstructed symbolic
derivation. Claims 1, 2, 3, and 5 have `HIGH` confidence. Claim 4 has `MEDIUM`
confidence because its proof chain imports Murari et al., Theorem 3.1 rather
than formalizing that antecedent in a proof assistant.

The numerical checks are deliberately not used as proof of the universal
statements. They independently exercise dimensions 16 and 32, 512 tokens,
1,024 complete activation regions, and depth 128. Five computed negative
controls fail for their theorem-specific reasons. A separate HF cpu-upgrade
falsification audit found no exact-claim counterexample and exposed two
wording boundaries:

- Claim 2's measure constant is finite for fixed parameters but not uniform
  over unbounded parameter choices.
- Claim 3's query constant is depth-independent, while its context constant
  may depend strongly on depth.

Historical d=1 evidence remains preserved and is labeled
`Historical rejected baseline`; it is not the basis of any current verdict.
