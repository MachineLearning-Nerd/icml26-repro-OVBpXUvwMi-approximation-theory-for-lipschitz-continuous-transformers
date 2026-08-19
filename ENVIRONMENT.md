# Environment and reproduction contract

## Fixed command

```bash
uv sync --frozen
uv run --frozen python run_reproduction.py
```

The current evidence uses Python `3.12`, the committed `uv.lock`, no GPU,
and one enforced worker for the Lean/Hugging Face Claim 4 job. Claim 4's
formal run used Lean `4.19.0`, mathlib `v4.19.0` at commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b`, and reported `164.06756182201207`
seconds with 64 logical CPUs visible. The fixed command, run IDs, and per-
claim runtimes are recorded under [`space/evidence/current`](space/evidence/current).

The numeric checks are deliberately downscaled corroboration: `d=16`, `d=32`,
512 tokens, 1,024 activation masks, and depth 128. They do not replace the
symbolic or Lean proof paths for universal claims.

This cleanup records and verifies the existing evidence bundle; it does not
silently replace it with an untracked rerun.

