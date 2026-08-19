# Audit report

This repository is an independent reproduction and claim audit for
**Approximation Theory for Lipschitz Continuous Transformers**.

All five explicit contracts pass. Claims 1, 2, 3, and 5 are supported by
symbolic, independent, or Lean-kernel evidence with high confidence. Claim 4
passes the abstract universal-approximation deduction and independent
publication gates, but remains medium confidence because the exact
matrix-level realization of the paper-class premises is source-audited rather
than fully encoded in Lean.

Read the detailed report at
[`reports/lipschitz-transformer/report.md`](reports/lipschitz-transformer/report.md),
the evaluator-facing current pages under [`space/pages`](space/pages), and
the release report at [`space/pages/release-report/page.md`](space/pages/release-report/page.md).

The branch roles and historical `orx/` to clean-name mapping are documented
in [`branch-audit.md`](branch-audit.md). Branch names describe evidence role;
they are not separate paper versions or author statements.

