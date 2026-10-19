# Assistant clean-environment cold run

Run UTC: 2026-10-19T15:54:38.028216+00:00. Operator: Codex assistant. Status: **PASS**.

Isolation: a new temporary project copy and a new Python virtual environment created with `python -m venv --without-pip`. No model package installation, credentials or data fetches. The current workspace's site-packages are not inherited.

Exact logical command: `<fresh-venv-python> <copied-project>/run.py --all --output <fresh-output>`. Temporary absolute paths are deliberately omitted from the public record.

First failure: None observed. Resolution: not needed if no failure. Measured setup and execution time: 0.728 seconds. Runtime and byte-for-byte output hashes are in `cold-run-receipt.json`.

Console output:

```
CRM 2026-08-27: watch/defer; causal range $74.36 to $298.02
Base $194.86; 22 checks passed; 0 failed.

```

All four deterministic financial/output files must match the frozen reference. The volatile run receipt is expected to have a new timestamp and is not compared. The course known answers, source checks, accounting/terminal/bridge checks, highest-risk SBC failure and decision-altering downside run inside this clean execution.

**No recording was made of a student performing this run.** This is useful technical reproduction evidence; it does not substitute for the student's Video2/code ownership or human AI-off locked changed-input exercise. Follow the README in a genuinely clean environment and record the required defense.
