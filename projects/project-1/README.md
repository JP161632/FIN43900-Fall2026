# Project 1 - NVIDIA (NVDA)

**WATCH / DEFER** at the historical September10,2026 US close of $218.36. Intended user: buy-side committee with no position; 12-24month decision horizon. Causal FCFF range roughly **$56-$212**, base about **$119**; consider initiation below roughly **$95** only with demand/collection/margin/commitment gates satisfied. These rounded figures are assumptions-driven outputs, not a live October quote. Exact executed numbers and all five-year statements are in [visible output](outputs/visible-output.md).

Start with [Student next steps](Student%20next%20steps.md): exact three-video recording routes, ~3minute scripts, human-evidence procedure and submission instructions. [Rubric audit](docs/rubric-audit.md) distinguishes verified technical work from missing human evidence. No full-score claim is made.

The [audited recording guide](docs/recording-guide.md) now uses **one fixed chart per video**. Open [Recording-Charts.pdf](Recording-Charts.pdf), page1forVideo1,page2forVideo2,page3forVideo3, and select Fitpage. Videos1/3 need no tabs or scrolling; Video2 has one brief actual-run terminal overlay. Separate1920x1080PNGs are in outputs/. Original source links remain on each chart. [recording-proof.html](outputs/recording-proof.html) is optional backup reading, not the default recording route. [Script audit](docs/recording-script-audit.md) explains the evidence alignment. Charts are preparation/presentation aids, not observed recordings or a substitute for authentic student evidence.

## Review without running

- [Decision-Memo.pdf](Decision-Memo.pdf): committee range, conditions and risks, <=2pages.
- [Research-Evolution.pdf](Research-Evolution.pdf): EditionA/B/addendum and prior NVIDIA lab corrections.
- [Validation-and-AI-Use.pdf](Validation-and-AI-Use.pdf): actual tests, evidence limits, named AI uses and lock status.
- [Visible output](outputs/visible-output.md): material inputs, statements, bridge, sensitivity, peer results and action.
- Open [dashboard.html](outputs/dashboard.html) locally in a browser for case/statement selectors and a clickable sensitivity grid. GitHub's source viewer does not execute HTML.
- [Source map](data/source-map.md), [driver challenge record](evidence/assumption-challenges.md), [peer policy](evidence/peer-policy.md), [transaction qualification](evidence/transaction-qualification.md).

## Reproduce offline

Python3.10+; engine is standard library only, no pip packages/network/secrets. From a terminal in this project folder:

```powershell
python run.py --all
python cold_run.py
```

Or from repository root: `python projects/project-1/run.py --all`. On this workspace Python is available as `.\.venv\Scripts\python.exe`. Source and output paths resolve from the script, not current directory. Validation failures exit nonzero with a diagnostic. Default outputs are deterministic except run-receipt timestamps. A cold run creates a new project copy and a no-pip virtual environment and compares four output hashes; the actual assistant run/log are retained in evidence/.

For isolated changed-input exploration (decimal rates):

```powershell
python run.py --case low --output .build/explore-low
python run.py --wacc 0.15 --growth 0.03 --output .build/explore-rate
```

Changed runs cannot overwrite outputs/ through this CLI. JSON input edits require `--all --output .build/<new-run>`; retain a single-input diff. Financial dates, units, nonpositive cash, invalid terminal growth and corrupted source totals can fail loudly. Do not hide a failure by deleting a cash flow or adding a cash/equity plug. No deployment or credentials are needed; .env is ignored and no .env.example is required.

## Data flow and conventions

`data/inputs.json` -> `model.py` statement forecast -> FCFF/terminal/WACC/ownershipbridge -> `run.py` results/visible report/interactiveHTML. `tests.py` checks independent known answers, source definitions, articulation, signs, boundaries, failures and decision effect. `build_package.py` creates Markdown records/scripts from executed output; `build_documents.py` renders PDFs using optional pinned requirements-docs.txt; `render_pdf_qa.py` renders every page. To rebuild optional PDFs: install requirements-docs.txt in a separate authoring environment, then run build_package.py, build_documents.py and render_pdf_qa.py. Do not regenerate final documents after adding authentic evidence without updating the generator/status text first; the present package honestly records pending student evidence.

Period: rolling years ending July26,2027-2031. Actual base statements reconcile to FY26 and H1FY26/H1FY27 filings and Jan/Jul balance sheets. LTM and46-day cash roll-forward are explicit transformations. CurrencyUSD, dollars/shares in millions, per-shareUSD, diluted proxy24,242M; no second split adjustment. Cash compensation substitutes for SBC, no addback/future dilution benefit; investment gains excluded. Terminalg3% with ROIC25% requires reinvestment. Operating leases stay operating; financial investments stay outside operatingNWC. Pending acquisition cash/retention, guarantee-loss and investment recovery assumptions are explicit. See source map/driver record for limitations and evidence needed before actual investment use.

## Existing NVIDIA labs and baseline

EditionA September1 Markdown is preserved byte-identical in evidence/, hash in Research-Evolution. Its 'initiate' is research admission. This rebuilt September10 EditionB reuses Labs5/8/10/11/12 with corrected classification, FCFF, signed flows and definition/timing boundaries. Prior-lab paths, hashes and last commits are indexed. No unrelated company content belongs in this active project folder.

**Supplied recordings:** [Video 1](https://www.youtube.com/watch?v=k8gWr7TUtx0) (2:53), [Video 2](https://www.youtube.com/watch?v=ASztkYCwwW8) (2:58), [Video 3](https://www.youtube.com/watch?v=m9quX8x7V3I) (3:00). Three transcripts are in docs/. Anonymous metadata access/durations checked; audiovisual performance not reviewed. [Video review](docs/video-review.md) logs student-requested editorial corrections of financial figures and associated terms. Audio alignment and observed timestamp indices remain unverified.

**Still required from student:** verify corrected text against audio and add observed timestamp indices; original checkpoint PDF/first Brightspace receipt; completed locked prediction/results or applicable documented instructor replacement; final playback/access checks and Brightspace final receipt. AI assistance: Codex based on GPT-6, October 19; exact backend version unexposed. The student must understand and defend submitted content.

Initial technical freeze: `project-1-nvidia-2026-10-19`. Prior recording snapshots remain immutable. Supplied video/transcript snapshot: `project-1-nvidia-peer-review-2026-10-19`; this is not certification of completeness. The manifest has 11 required entries plus optional deployment; file-integrity.json and publication-audit.json record hashes/access. GitHub is not Brightspace submission.

Authoring order after changes: `build_package.py`, `build_documents.py`, `render_pdf_qa.py`, `build_recording_charts.py`, then `build_recording_evidence.py` to refresh actual PDF heading pages, charts, backup proof panels and recording scripts. The final command regenerates Student next steps.md from the recording-guide template and actual saved values. Finance results remain unchanged by this documentation-only build.

PDF design review: all seven project PDF files (13 unique pages) were checked for layout, evidence links and numerical consistency. See [PDF quality/rubric review](docs/pdf-quality-audit.md). The document builder uses clean Markdown templates in docs/templates/; baseline source bytes and supplied transcripts are protected. Run audit_documents.py after rebuilding.

Attributed peer review: student-confirmed Antigravity log of October 1, credit **peer challenge**. See [review and dispositions](evidence/partner-review-record.md); [independent checks](outputs/peer-review-checks.json). Equal relative shocks make margin the larger tested valuation driver. Student terminal-growth prediction is preserved before a new run; exact new rate/action remain pending.
