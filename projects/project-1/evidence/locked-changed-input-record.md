# Locked Changed-Input Record: student terminal-growth test

Status: **EXECUTED. Student prediction and exact input/action specification were committed before execution.** Direction and expected committee action match; observed magnitude is modest. Instructor permission for AI-assisted wording was previously reported by the student; the assistant recorded/executed the test and does not invent an independent AI-off attestation.

## Student prediction and immutable precommit

Original student wording remains in student-terminal-growth-prediction.md, initially committed at **d9f1f52**. Follow-up messages supplied **2.5%** and **WATCH / DEFER remains**. Complete specification: **5a9de1da7f280857b3c132af59f06e76a58faff0**, committed **2026-10-19T16:54:56-04:00** (20:54:56 UTC), before the run began at **2026-10-19T20:55:33.484427+00:00**. The preservation time for the completed specification is 20:54:17 UTC, not an invented earlier composition time.

Readable restatement of the student's committed prediction: lower terminal growth should lower valuation because long-run growth is slower; WATCH / DEFER should remain. The original described valuation as “mch lower” without a numerical threshold. This summary does not replace the original pre-run words.

| Required field | Observed record |
|---|---|
| Human prediction author | Student, supplied through conversation before execution |
| Input and units | cases.base.terminal_growth via --growth; annual nominal decimal rate |
| Old / new | 0.03 / 0.025 = 3.0% / 2.5%; -0.5 percentage point / -50bp |
| Expected direction and reason | Lower value because long-run growth is lower |
| Expected action / decision effect | WATCH / DEFER remains |
| Immutable specification | Commit 5a9de1da7f280857b3c132af59f06e76a58faff0; specification hash in locked-growth-results.json |
| Baseline output | $118.58486735/share; EV $2,793,797.327341m; equity $2,874,734.354339m; WATCH / DEFER |
| Changed output | $116.56710034/share; EV $2,744,882.619468m; equity $2,825,819.646466m; WATCH / DEFER |
| Actual direction / size | Lower by $2.01776701/share (-1.7015%) |
| Expected vs actual action | Both WATCH / DEFER; expected action matches |
| Magnitude comparison | Direction supported. A 1.70% decrease is modest; no quantitative “much lower” prediction was specified or certified |
| Failure diagnosis | No execution/direction failure. Lower growth also lowers required terminal reinvestment, offsetting part of the price decline |
| Why action is unchanged | $218.36 market price remains above changed value $116.57 and 20%-discount entry ceiling $93.25 |
| Held fixed | Identical five-year statements/FCFF, WACC, terminal ROIC, diluted shares and bridge assumptions |
| Executor / timing | Assistant; actual baseline/changed logs preserved after the precommit |

## Actual commands and retained artifacts

From the project folder, the executed commands were:

```
python run.py --growth 0.03 --output evidence/locked-growth/baseline
python run.py --growth 0.025 --output evidence/locked-growth/changed
```

The commands were invoked using the workspace Python interpreter. Exact stdout, stderr, return codes and UTC run times are in each execution-log.json. Both returned exit code zero.

- Baseline: `evidence/locked-growth/baseline/scenario.json`; SHA-256 `8b797ab0e61bc9634fe84c62fc3aafdede0cd9b05eb3d1a750dd4a9384f37cb3`.
- Changed: `evidence/locked-growth/changed/scenario.json`; SHA-256 `839d6ef721a863df333cf3790c2e71202494e1d36e2f6bb83c3e29b814c0ca14`.
- Consolidated receipt, commit/time, specification, all hashes and comparisons: evidence/locked-growth-results.json.
- Reproduction/guards: run_locked_growth_test.py; it refuses to overwrite these historical run artifacts.

## Financial explanation and decision effect

WACC stays 13.8965%; terminal ROIC stays 25%. Required terminal reinvestment falls from g/ROIC = **12% to 10%**. Consequently, terminal FCFF rises from **$373,739.90m to $380,378.49m**, even though terminal growth falls. The larger WACC-minus-growth denominator more than offsets that increase: discounted terminal value falls from **$1,819,080.17m to $1,770,165.46m**. Explicit operating forecasts remain unchanged. This explains why the total valuation decrease is smaller than the student's qualitative expectation might suggest.

The result reinforces deferral; it does not create a buy signal or prove forecast accuracy. The frozen base case remains g=3%; this is a separately preserved sensitivity exercise, not a silent replacement of the base valuation.

## Authorship and policy boundary

The student's own prediction, chosen 2.5% input and expected unchanged recommendation precede the execution. The assistant transcribed the record, ran the code and formatted results. The student's reported in-class permission covers AI-assisted wording; the supplied record documents that basis without claiming an AI-off attestation that was not provided. Earlier AI-authored WACC tests remain separate and are not relabeled as this student prediction.
