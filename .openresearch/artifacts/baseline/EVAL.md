# Historical rejected baseline

This baseline reproduces the evidence judged at 5/10. It is intentionally
classified as toy evidence, not as verification of any universal theorem.

Run:

```bash
uv run --frozen python run_reproduction.py
```

The verifier exits nonzero if any recorded baseline check fails. Its successful
exit only means the historical toy calculations regenerated.
