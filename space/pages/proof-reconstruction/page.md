# Independent proof reconstruction

The exact derivation is downloadable as
[`symbolic_derivation.md`](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/symbolic_derivation.md).
The certificate contains 25 ordered nodes, and the verifier rejects a missing,
extra, reordered, renamed, or source-mismatched node.

## Dependency chain

```text
ReLU potential -> segment Jacobian -> PSD spectrum -> Claim 1
log partition -> covariance Hessian -> cocoercivity -> Claim 2
Claims 1+2 -> pushforward recurrence -> Claim 3
strict scaling -> compact min cover -> compact max cover -> Claim 5
parallel lattice + KR witness + scalar ResNet density + Claim 5 -> Claim 4
```

## Non-circularity

No approximation target is selected and no basis is fit. Claim 5 is proved for
an arbitrary target by strict-margin scaling and two finite compact subcovers.
Claim 4 verifies lattice closure and strict point separation for the whole
Transformer class. The four-point envelope is only an independent complete
finite-domain sanity check.

## Source identity and anchors

- arXiv source: `https://export.arxiv.org/e-print/2602.15503`
- retrieved: 2026-07-30
- SHA-256:
  `d7d496f38d43b90a9056463183dd7368c4e620af49324a8b16f43f5d67dc80a2`
- Claim 1: equation `eq:1lipMLP`, Lemma `lem:MLP-Lip`
- Claim 2: Lemma `lem:property-in-context-map-1`
- Claim 3: Lemma `lem:property-in-context-map-2`
- Claim 4: Theorem `thm:main-approximation`
- Claim 5: Lemma `lem:mod-RSW`

[Source manifest](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/evidence/current/source_manifest.json)
and
[executable verifier](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/reproduction/proof_verifier.py).
