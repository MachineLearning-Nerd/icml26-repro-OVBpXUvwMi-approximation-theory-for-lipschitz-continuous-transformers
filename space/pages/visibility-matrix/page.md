# Evaluator visibility matrix

Traversal starts at `README.md` or `pages/index.md`, then
[Current verification](#/current-verification). Every claim page states the
exact contract, assumptions, quantifiers, verdict, limitations, command, SHA,
seeds, CPU/runtime, inline result, and direct raw links.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/claim-1-current) | yes | yes | yes | yes | yes | yes | release-ready |
| 2 | [Claim 2](#/claim-2-current) | yes | yes | yes | yes | yes | yes | release-ready with fixed-parameter scope explicit |
| 3 | [Claim 3](#/claim-3-current) | yes | yes | yes | yes | yes | yes | release-ready with depth dependence explicit |
| 4 | [Claim 4](#/claim-4-current) | yes | yes | yes | yes | yes | yes | release-ready; MEDIUM antecedent-formalization risk |
| 5 | [Claim 5](#/claim-5-current) | yes | yes | yes | yes | yes | yes | release-ready |

Environment files:
[`pyproject.toml`](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/pyproject.toml),
[`uv.lock`](https://huggingface.co/spaces/DineshAI/OVBpXUvwMi/blob/main/uv.lock).

Historical judged files remain reachable through
[Historical rejected baseline](#/historical-rejected-baseline), but none is
the apparent current verifier.
