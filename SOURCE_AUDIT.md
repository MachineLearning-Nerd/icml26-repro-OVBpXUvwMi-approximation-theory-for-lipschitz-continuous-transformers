# Source audit

The claim contracts use the arXiv source for **Approximation Theory for
Lipschitz Continuous Transformers**, retrieved on `2026-07-30`.

| Source | URL | SHA-256 |
| --- | --- | --- |
| e-print source archive | https://export.arxiv.org/e-print/2602.15503 | `d7d496f38d43b90a9056463183dd7368c4e620af49324a8b16f43f5d67dc80a2` |
| ar5iv HTML | https://ar5iv.labs.arxiv.org/html/2602.15503 | `c4996a8ecb30cad3e652faf70a2c29430fc8d3a58c682e3535d4837f2a4ce1e5` |

Claim anchors are Lemma 1 (`eq:1lipMLP`, `lem:MLP-Lip`), Lemma 2
(`lem:property-in-context-map-1`), Lemma 6
(`lem:property-in-context-map-2`), Theorem 8 (`thm:main-approximation`),
and Lemma 9 (`lem:mod-RSW`).

The exact matrix-level construction that establishes the paper-class
nonemptiness, lattice closure, and strict two-point interpolation premises in
Claim 4 is source-audited and executable algebraically, but is not encoded as
Lean matrices. That is the reason for the medium-confidence label. The
restricted Stone–Weierstrass deduction itself is Lean-kernel checked without
`sorryAx`; its deliberately false strict-margin and coefficient-sign
controls fail as expected.

The current source manifest, referenced papers, and release hashes are under
[`space/evidence/current`](space/evidence/current).

