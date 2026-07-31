# Evaluator-blind red team

The reviewer was given only a fresh candidate assembled from the exact judged
Space revision plus the text upload allowlist. It began at `README.md`,
`logbook.json`, and `pages/index.md`; no OpenResearch logs, unpublished
branches, or repository knowledge were used.

## First pass — failed and fixed

Files opened:

```text
README.md
logbook.json
pages/index.md
pages/current-verification/page.md
pages/claim-1-current/page.md
pages/claim-2-current/page.md
pages/claim-3-current/page.md
pages/claim-4-current/page.md
pages/claim-5-current/page.md
pages/proof-reconstruction/page.md
pages/visibility-matrix/page.md
pages/release-report/page.md
pages/red-team/page.md
pages/overview/page.md
pages/claims/page.md
pages/evidence/page.md
pages/conclusion/page.md
pages/verification-run/page.md
evidence/current/judged-space-manifest.sha256
```

Two conclusions could not be verified:

1. `evidence/current/proof_dag.json` was linked but absent from the allowlist.
   The link was corrected to the uploaded `reproduction/proof_dag.json`.
2. Claim 4 described its residual risk but lacked an explicit `Limitation`
   heading. The heading was added.

All 17 judged files were present and the secret scan had zero hits.

## Second pass

The candidate was rebuilt again from a new download of the exact judged
revision. The same 19 files above were opened, plus 43 directly linked raw/code
files were resolved inside the candidate.

Result:

```json
{
  "claim_pages_passed": 5,
  "historical_files_expected": 17,
  "historical_files_missing": 0,
  "missing_links": 0,
  "secret_hits": 0,
  "conclusions_not_verified": 0,
  "tree_sha256": "b2bba261f2abf859d2266e91778e122d7126ef4ea85ec274425a082b59e942ea",
  "passed": true
}
```

The upload-file manifest for that build contained 74 text files and had
SHA-256
`6abc4fbfd24b18cd57152a2d0358317a1c100816aca7ed364995e636180783d9`.
The manifest is regenerated after final editorial changes and checked again
before upload.
