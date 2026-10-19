# Student next steps

This is the exact recording/submission handoff for the NVIDIA Project1 package. Scripts are **AI-written preparation**, not transcripts or proof that you performed a task. Read, understand and personalize them; say only what you can explain and actually did. You cannot get full credit from videos alone while the human evidence below is missing.

## Complete these before recording

1. Recover the original EditionA PDF and first successful Brightspace checkpoint receipt. Do not recreate or alter them. The unchanged NVIDIA Markdown is already preserved and typeset as a reading appendix, but it is not proof of the submitted PDF/receipt. If never submitted, tell the instructor and request how to handle the missing checkpoint; no AI can backdate compliance. EditionB date addendum is already documented.
2. Confirm whether October 1 Lab12's reported partner answers came from a real discussion. If so, verify exact wording/role/date, avoid private information and record what actually changed with independent evidence. If draft/AI-written or uncertain, leave them qualified and obtain actual partner review. A clearly marked fictional sample is in evidence/assumption-challenges.md; never claim it was spoken. Record the real challenge and response; the model need not change if you can justify why.
3. Complete the **human AI-off locked changed-input exercise** below. You must author the prediction yourself before the run. This cannot be filled retrospectively by AI. The assistant's existing WACC test does not count as your human lock.
4. Open outputs/dashboard.html locally in a browser and check labels. Open outputs/visible-output.md, Research-Evolution.pdf, Decision-Memo.pdf and Validation-and-AI-Use.pdf. Check that the numbers below still match outputs/results.json. Use the included dated historical valuation; do not describe $218.36 as today's quote.

## Human AI-off lock - exact procedure

Close AI tools for the prediction. In evidence/locked-changed-input-record.md, write your own name/role as appropriate under course privacy rules, actual UTC time, one load-bearing input you independently choose, its JSON path, old/new numeric values and units, why you expect a direction, expected enterprise/share-value direction and expected committee-action effect. Do not copy the assistant WACC prediction or invent an earlier timestamp. Do not run or edit the model until the prediction is saved and committed.

From the repository root, while prediction exists and before changing input/running:

```powershell
git add -- projects/project-1/evidence/locked-changed-input-record.md
git commit -m "Lock my AI-off prediction before changed-input run"
git rev-parse HEAD
git show -s --format=%cI HEAD
```

Save that commit ID/time in a **separate** results addendum after the run, retaining the original committed prediction. Run an unchanged baseline into .build/student-baseline, edit just your chosen field in data/inputs.json using a text editor, then run into .build/student-changed. These commands assume your terminal is at the repository root and Python3.10+ is installed:

```powershell
python projects/project-1/run.py --all --output projects/project-1/.build/student-baseline
python projects/project-1/run.py --all --output projects/project-1/.build/student-changed
```

Execute the second command only after making the single edit. Preserve both results.json files in evidence/student-lock-baseline.json and evidence/student-lock-changed.json; include actual values, direction, action and decision threshold, diagnosis if wrong or no-change reason. Capture console exit/failure messages; an honest failed prediction is useful if diagnosed. Restore **only your own single input edit** from the original value; do not use a destructive repository reset. Rerun normal outputs and compare their hashes with the frozen snapshot. Have the assistant audit your completed record after you provide it. The final PDF/manifest/freeze must be regenerated to include authentic evidence, not left marked pending.

## Setup for all three videos

Use screen recording with clear audio and a small webcam view unless your instructor approved an accommodation. 1080p, browser zoom125-150%, hide notifications/private tabs, keep financial rows readable. Say “NVIDIA” and “free cash flow to the firm”; distinguish millions from billions. Record three separate files. Aim Video1 2:40-2:55 (hard maximum3:00), Video2 about3:00 (maximum5:00), Video3 about3:00 (maximum5:00). Practice once; scripts are roughly three minutes at a clear speaking pace with short cursor pauses. Trim dead time, not substantive evidence.

Use a fresh clone or separate folder and a fresh Python environment for the cold run. From a terminal in the Project1 directory:

```powershell
python -m venv .build/student-venv
.\.build\student-venv\Scripts\python.exe run.py --all --output .build/student-cold-output
```

No pip install is required for the engine. On macOS/Linux use .build/student-venv/bin/python. Keep the terminal/output and actual first failure/resolution (if any). The assistant already ran cold_run.py in a clean no-pip environment; the receipt honestly identifies the assistant. **Your recording must show your own clean run**, and your log should identify you and the actual observed result. Do not describe the assistant receipt as your run.

## Video1 - research evolution, target2:50; maximum3:00

Record these screens in this order; all timings are **planned**, replace with observed indices later:

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | Research-Evolution.pdf first page, baseline/addendum | September 1 admission thesis versus September 10 decision; checkpoint evidence status. |
| 0:35-1:15 | Same PDF A-to-B table, then original Lab10/11 writeups if legible | Financial investment classification and signed cash-flow error corrected. |
| 1:15-1:55 | data/source-map.md share/investment/debt reconciliation; optionally SEC Q2Note5 in another tab | Independent source check, exact basis and dates, no AI agreement as validation. |
| 1:55-2:30 | evidence/assumption-challenges.md, prior Lab12 and actual confirmed partner entry | Actual challenge/disposition, qualified attribution, what changes the forecast. |
| 2:30-2:50 | outputs/visible-output.md top | Final range/action, real remaining evidence status. |

Script (read naturally, about3minutes; use the truthful status sentence specified below):

“This project asks whether a fund with no NVIDIA position should initiate, watch or defer, or not initiate over a twelve-to-twenty-four-month horizon. I used my earlier NVIDIA labs as the research trail. EditionA was dated September first. Its word ‘initiate’ meant start valuation research, not buy the stock. EditionB uses the September tenth close, and that date change is disclosed.

The biggest improvement was connecting the operating forecast to a defensible valuation. Lab10 had company-specific growth, margin, working-capital and equipment drivers, but broad other-assets balances mixed operating items with financial investments. Lab11 also identified problems with labeling cash after distributions and handling negative cash flows. Those errors could produce a model that balances while still valuing the wrong economics.

The rebuilt model separates financial investments from operating working capital, keeps signed cash flows, and discounts free cash flow to the firm at WACC. I checked definitions against NVIDIA's filing and its earnings release. At July twenty-sixth, cash plus debt securities was fifty-six-point-six billion dollars. Marketable equity holdings were separate. Debt also increased substantially, so the earlier annual debt balance was stale.

The review question I focus on is whether Data Center growth is durable. Supplier commitments tell us what NVIDIA may have to buy; they do not prove customers will accept systems and pay. That distinction affects the growth, inventory, collection and downside assumptions. The challenge record distinguishes verified finance evidence, qualified prior discussion and a fictional AI practice answer. A generated practice answer is not partner evidence.

The resulting causal range is about 56 to 212 dollars per share, with a base reference around 119. At the dated price of two hundred eighteen dollars and thirty-six cents, I would watch or defer. I would reconsider only with a sufficient price cushion and evidence supporting demand, cash collection and margins. The original checkpoint receipt, the human prediction exercise and the recordings are separate evidence requirements; the status record identifies what is actually complete.”

Before recording: if you have supplied the original checkpoint/lock/partner evidence and we updated the package, replace only the last status sentence with the factual completed status. Never say you submitted or completed evidence unless you did. The script does not invent a past partner quote.

## Video2 - code ownership and validation, target3:00; maximum5:00

Prepare code tabs before recording: data/inputs.json; model.py at forecast, valuation and dcf_cashflows; outputs/validation-results.json; your genuine locked record/addendum. Open terminal in a fresh project copy/environment as above. Record the command execution, not only a screenshot.

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | inputs.json then model.py forecast | Fact/assumption separation; statement driver to FCFF. |
| 0:35-1:10 | model.py near cash/equity checks and valuation terminal | No balancing plug; retainedSBCcost; g/ROIC reinvestment. |
| 1:10-1:45 | Terminal: run fresh-venv command shown above | End-to-end result and actual15tests; first failure/resolution if present. |
| 1:45-2:25 | outputs/validation-results.json: officialknownanswers, contamination experiment, downside | Expected values from course answers; highest-risk deliberately wrong input. |
| 2:25-3:00 | Your locked record at precommit plus actual-results addendum | Show author/time/immutablecommit, old/new units, prediction BEFORErun, actualdirection/action and diagnosis. |

Script:

“The application runs locally with Python's standard library. The input file separates reported history, market observations, common forecast assumptions and causal cases. The source map gives the date, definition and transformation for each material input group. It needs no credentials or live data connection.

The forecast function starts with the July balance sheet and produces five rolling years of income, balance-sheet and cash-flow statements. Data Center and Edge revenue drive margins and expenses. Collection days, inventory days and payment days drive working capital. Capital spending and depreciation roll property and equipment forward. Cash comes from operating, investing and financing flows. Equity comes from retained income and distributions; neither is a balancing plug.

Free cash flow to the firm starts with after-tax operating profit, adds depreciation and amortization, and subtracts operating capital spending and working-capital investment. Stock compensation remains an economic cost through cash replacement. Financial investments and dividends are kept outside FCFF. The terminal calculation requires reinvestment equal to growth divided by terminal return on invested capital, so perpetual growth is not free.

I am now running the project in this fresh environment. The visible output reports the decision and the validation count. The test file compares the DCF engine with the course's independently published answers, including all nine sensitivity cells. Other tests check statement articulation, cash, equity, valuation bridges and the expected effect of discount rates and terminal growth.

The highest-risk experiment deliberately repeats the old investment-classification mistake. Scaling the investment portfolio as operating working capital creates false cash investment. Another failure test forces an unsupported cash deficit and requires the model to stop. Negative cash flows are preserved instead of silently dropped.

The required human locked exercise is separate from the assistant's WACC test. Here I show the record's actual status, the prediction commit if completed, and the observed results if available. A complete record needs my own AI-off prediction before execution, old and new units, actual valuation direction, decision effect, and a diagnosis or a threshold-based reason the action stayed unchanged. I do not claim missing evidence as completed.”

For maximum-credit completion, finish the human exercise first and use the final30seconds to **read your actual old/new values, predicted/actual direction and action effect from your record**, in your words. This intentionally cannot supply a prediction for you. If incomplete, the honest pending line above is accurate but leaves rubric points unresolved.

## Video3 - committee defense and live product demo, target3:00; maximum5:00

Use outputs/dashboard.html in your browser. This is a locally opened interactive artifact, not a deployed website. Pre-open Decision-Memo.pdf in another tab. Keep most recording time on the running product. Selectors display executed engine results; they do not run a live market-data calculation.

| Time | Exact screen/action | Point to show |
|---|---|---|
| 0:00-0:35 | Dashboard base case cards | User, date, market, range and conditionalaction. |
| 0:35-1:05 | Scroll to EV/common-equity bridge; change Statement to Cashflow | Cash/investments/debt/dilution plus operating source ofvalue. |
| 1:05-1:40 | Scroll to WACC-growth grid; click a row; show reverseDCF | Sensitivity, terminal dependence and market-impliedgrowth. |
| 1:40-2:15 | Return case selector, choose low | Actual case value/action changes, explain causalinputs. |
| 2:15-2:35 | Choose high then base | Upside conditions, range rather than single target. |
| 2:35-3:00 | Memo page2 monitoring/conditions, then dashboardbase | Committee ask and exact reversal triggers. |

Script:

“My committee recommendation is watch or defer. The fund has no position, so it can wait for a price that compensates for uncertainty. This application values NVIDIA at the September tenth, twenty-twenty-six close of two hundred eighteen dollars and thirty-six cents. My causal intrinsic range is about 56 to 212 dollars per share. The base reference is about 119; it is not a precise target or a probability-weighted forecast.

Here is the enterprise-to-equity bridge. Operating value comes from five years of statement-driven FCFF and a reinvestment-supported terminal value. The bridge then handles cash, financial investments, debt, acquisition costs and other claims separately. The diluted share proxy is twenty-four-point-two-four-two billion. Investment holdings are not treated as cash or scaled with operating revenue.

The base discount rate is about 13.9 percent, and terminal growth is three percent. About 65 percent of enterprise value comes from the terminal value, which limits confidence. This sensitivity grid shows how discount rate and growth affect value. The market-implied test requires roughly 20 extra percentage points of Data Center growth in every explicit year, if all other base assumptions remain fixed. That is a demanding conditional expectation, not proof the market is wrong.

I am switching to the low case. Deployment and financing slow, margins weaken, collections take longer and inventory builds. Supply losses and guarantee exposure compound the pressure. Value falls to about 56 dollars, and the risk gate changes the action to do not initiate. Supplier commitments are an obligation risk, not a guaranteed sales backlog.

The high case requires stronger, durable demand and better execution, and reaches about 212 dollars. Peer multiples suggest different market expectations, but AMD and Broadcom have different margins and business mixes, and historical earnings lag current growth. I do not average those prices with the DCF.

I would consider initiation only below roughly 95 dollars using the refreshed base estimate, with demand, collections, margins and commitments validated. Sustained Data Center growth below twenty percent, collection days above ninety-five, gross margin below seventy percent or material guarantee losses would push me toward no initiation. The committee's action today is to keep NVIDIA on watch and require that evidence before committing capital.”

## After recording - final review and freeze

1. Save distinct Video1/2/3 recordings; use stable unlisted hosting or repository-compatible links the instructor can access. Don't commit large raw recordings to Git. Keep titles and durations factual. Only you can grant/upload from accounts unavailable to the assistant.
2. Replace docs/transcript-video-1.txt, -2.txt and -3.txt with corrected **actual** transcripts and observed timestamp indices. Fix NVIDIA/NVDA, FCFF, WACC, period dates, figures, sources and attribution. Do not paste preparation scripts unless they match what you actually said.
3. Provide the video URLs, actual durations, actual transcripts and completed checkpoint/locked/partner evidence for a final consistency review. The assistant can audit supplied evidence, update PDFs/status/manifest and create a **new** final freeze tag. The current technical tag must remain immutable; it is not a claim videos are complete.
4. Test repository and every video/transcript link in a logged-out/incognito browser; confirm audio, readable output and captions. Ensure the instructional team can access private/unlisted items. Record observed check times, not assumed access.
5. Fill submission-manifest.csv with final stable URLs, titles, durations, observed timestampindices, accesschecks and finaltag/filehashes. Include all11requiredrows; optionaldeploymentcanremainunused.
6. Submit the seven-part final bundle through the **final assignment** Brightspace page by October 19,2026 at11:59PM course time, and save the successful receipt. The EditionA checkpoint has its separate designated submission page. GitHub upload does not submit Brightspace. No grade is guaranteed; inspect the current docs/rubric-audit.md for unresolved requirements.
