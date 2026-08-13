# Branch audit

This repository began with OpenResearch-style `orx/` branch names. The clean
names preserve the branch history while making each branch's purpose clear.
`main` is the public documentation and evidence surface.

| Historical branch | Clean branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Publication surface and cumulative evidence |
| `orx/judged-toy-baseline` | `audit/judged-toy-baseline` | Preserve the historical `d=1` judged baseline |
| `orx/direct-symbolic-proof-certificates` | `audit/direct-symbolic-proof-certificates` | Add the 25-node symbolic proof DAG and independent checks |
| `orx/assumption-satisfying-falsification-audit` | `audit/assumption-satisfying-falsification` | Search exact-claim boundaries and premise-satisfying counterexamples |
| `orx/cumulative-evaluator-visible-release-candidate` | `release/cumulative-evaluator-candidate` | Assemble cumulative evaluator-visible evidence |
| `orx/release-gated-publication-artifact` | `release/release-gated-artifact` | Build the first release-gated report and publication artifact |
| `orx/lean-formal-verification-for-claims-4-and-5` | `formal/claims-4-and-5-lean` | Formalize the compact-space density arguments in Lean |
| `orx/evaluator-visible-claims-4-and-5-formal-evidence` | `release/evaluator-claims-4-and-5` | Publish the current Claims 4/5 evidence and navigation |
| `orx/publish-lean-claims-4-and-5-evidence-to-main` | `integration/published-lean-evidence` | Integrate the published Lean evidence into `main` |

Branch hygiene after publication:

- nine public branches remain: `main`, four `audit/` or `formal/` evidence
  branches, and four `release/` or `integration/` publication branches;
- every historical `orx/*` reference is removed from GitHub;
- the README and report link only to clean branch names; and
- the published history is attributed to `MachineLearning-Nerd` with the
  account's noreply address.
