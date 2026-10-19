# Student next steps - audited recording guide

**Use this guide instead of the earlier recording route.** It is also saved as `Student next steps.md` in the Project1 folder. Every timed scene below names the question it proves, the exact file/heading to show and the evidence to point at. Timings are planning targets; replace them with observed indices after recording. Scripts are preparation aids, not actual transcripts.

## What the three videos must prove

The course's Week7 handout gives three distinct questions:

| Video | Exact evidence question | What your recording must demonstrate |
|---|---|---|
| 1 | What changed or remained stable after project-specific research; what drove it; and what evidence justified it? | Earlier view/value -> a sourced challenge/correction -> revised assumptions/value -> changed or unchanged decision. Identify course, prior-lab, AI and qualified peer contributions accurately. |
| 2 | How does the submitted code produce the result, and what high-risk test passed or failed? | Trace one company driver through statements/FCFF/valuation, run the application, and show numerical known-answer/changed-input/failure evidence. A PASS count alone is insufficient. |
| 3 | What should the committee do, under what conditions, and what would reverse the decision? | Defend dated action/range, method disagreement, downside and measurable entry/reversal triggers. The product supports your argument; the video is not a feature tour. |

Source: `lessons/week-07/student-handout.md`, “Three evidence surfaces”; attribution guidance: `projects/templates/research-evolution-template.md`. Maximum3:00 for Video1; maximum5:00 each for Video2/3. Aim Video1 2:45-2:55 and Videos2/3 approximately3:00-3:30; slow down rather than racing through important evidence. Course checklist sets the limits; the timings below are suggested routes, not extra course requirements. Webcam overlay is optional here unless the instructor separately requires it; prioritize legible screens and clear audio.

## Open these tabs before recording

All paths below start at `projects/project-1/` unless marked **course repository**. Open Markdown in VS Code's preview (Ctrl+Shift+V) or GitHub's rendered view, not a tiny raw-text pane. Use browser/PDF zoom125-150%. Hide private tabs/notifications.

| Tab | Open this exact file | Park it here |
|---|---|---|
| A | `Research-Evolution.pdf` | Page3, “Initial thesis - initiate” in the preserved EditionA reading appendix. The original submitted PDF/receipt, if supplied, is preferable for proving actual checkpoint history. |
| B | **Course repository:** `projects/lab-05-nvda-dcf/nvda-dcf-lab.md` | Ctrl+F **“I — NVIDIA through the model”**; show “Value per diluted share” and then scroll slightly to **“E — Sensitivity grid and reverse DCF.”** |
| C | `outputs/recording-proof.html` | Open locally in a browser. Buttons jump to Research evolution, Numerical validation or Committee evidence. This is a reading aid generated from actual saved results, with links to the underlying artifacts. It does not create new test runs. |
| D | NVIDIA Q2 10-Q | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm ; browser Ctrl+F **“42,783”**. Show the balance-sheet row label and July26/January25 column headings. The exact rows are copied in proof panelR3 for readability if the SEC site cannot load. |
| E | `data/inputs.json` and `model.py` in editor tabs | inputs: Ctrl+F **`"dso":75`**. model: Ctrl+F **`b['ar']=`**, then **`fcff=nopat`**, then **`terminal=rows`**. Code anchors are safer than line numbers, which change with edits. |
| F | Terminal | Course repository root, the `FIN43900-Fall2026` folder. Prepare the fresh-venv command below before Video2. |
| G | `outputs/dashboard.html` | Open locally by double-clicking it in File Explorer; select **base** and **Income statement**. GitHub source preview does not run HTML. |
| H | `Decision-Memo.pdf` | Page1 “Committee ask and valuation range.” Page2 “Disagreement across methods and market expectations,” then “Conditions, reversal triggers and next evidence.” |

You need A-D for Video1, C/E/F for Video2 and C/G/H for Video3. Do not switch through every file in the repository. Keep this guide or printed script outside the recorded screen.

## Video1 - research evolution with defensible values

The strongest story is **research admission -> initial dated valuation -> identified limits -> corrected/current valuation -> decision held with stricter conditions**. Do not claim that EditionA recommended buying. Do not describe the entire price-estimate change as the impact of AI or one corrected input. Lab5's grid interval and the final causal interval have different definitions.

| Planned time | Exact screen and scroll/action | Claim the visible evidence proves |
|---|---|---|
| 0:00-0:25 | TabA, page3, **“Initial thesis - initiate.”** Point to the sentence saying preliminary research admission, not a buy recommendation. | The original question and uncertainty existed before the completed valuation. Do not call this newly typeset appendix an original checkpoint receipt. |
| 0:25-0:55 | TabB, **“I — NVIDIA through the model.”** Point to **62.7184**, then the grid's **55.59 / 72.40** endpoints and **15.88%** base WACC. | A concrete earlier valuation existed. It used annual data/annual weighted shares, not the final rolling forecast. |
| 0:55-1:35 | TabC, **Research evolution**, panel **R1 Before and after**, then **R2 Why it changed / attribution**. | Annual revenue215,938 -> LTM302,970; WACC15.88% ->13.90%; share basis24,514 ->24,242; final base$118.58. Multiple basis/assumption changes mean no single-cause price bridge. |
| 1:35-2:05 | TabD, find **42,783**. Keep cash22,443, debt securities34,143 and equity securities42,783 visible with labels/date. | Independent primary evidence supports separating investments from operatingNWC/cash. This is stronger than showing only our own source ledger. |
| 2:05-2:30 | TabC, **R3 Independent correction and test**, then **R4 What changed the judgment**. | Source-backed classification, a quantified diagnostic and a challengeable forecast support the revision. Show the prior-lab limitation rather than claim the model was right merely because it balanced. |
| 2:30-2:55 | TabC, **R4** current value/action card. | Final causal range$55.93-$212.08, base$118.58, date and price218.36, watch/defer held from Lab5 to finalB. Uncertainty changes conditions rather than disappearing. |

Script:

<!-- SCRIPT1 -->
“My research began with a question, not a buy recommendation: could NVIDIA turn rapid Data Center growth into durable owner cash flows at a reasonable price? EditionA admitted NVIDIA for deeper research.

The first completed DCF, in Lab5, estimated sixty-two dollars and seventy-two cents per share. Its discount-rate and terminal-growth grid ran from about fifty-six to seventy-two dollars. It used the annual filing, a fifteen-point-eight-eight-percent WACC and annual weighted diluted shares. Its watch-defer conclusion was conditional, and the reverse-DCF search did not find a solution within its limited bracket.

The later labs exposed why I should not simply carry that number forward. Lab11 withheld a new valuation while investment classification, cash-flow labels and terminal assumptions remained unresolved. Those are finance problems that a balanced spreadsheet cannot rule out.

Here is the independent filing check. July cash and debt securities total fifty-six-point-six billion dollars, while marketable equity investments are a separate forty-two-point-eight billion. Financial holdings should not grow automatically as operating working capital, and unrealized investment gains are not operating cash generation.

The revised model uses a trailing operating base, five linked statements and an explicit ownership bridge. First-year FCFF is about one hundred ninety-one billion, versus one hundred thirty-one billion in Lab5, with different forecast windows. Its base reference is about one hundred nineteen dollars, with a causal range of fifty-six to two hundred twelve. That range is a set of different operating cases, not the same sensitivity interval as Lab5. The value change also reflects the reporting base, forecast, WACC, terminal reinvestment and share basis; I cannot assign it all to one correction.

Course requirements drove the FCFF architecture. Earlier labs recorded the limitations. AI assisted the rebuild and checks; filings and numerical tests support accepting or qualifying its output. Growth, discount-rate and investment-recovery choices remain assumptions to challenge.

The later watch-defer action held at the dated two-hundred-eighteen-dollar market price. What evolved was the evidence and the conditions for acting, not a claim that uncertainty disappeared.”
<!-- /SCRIPT1 -->

If you discuss a real partner contribution, use your completed actual review record and replace a sentence about earlier lab limitations with that specific challenge and its tested effect. Do not read a fictional practice response as partner testimony. The existing Lab12 discussion is qualified until attribution is confirmed.

## Video2 - code to output, numerical benchmark and high-risk test

Prepare the new no-pip environment **before recording**, from the course repository root:

```powershell
.\.venv\Scripts\python.exe -m venv --without-pip projects/project-1/.build/video-venv
```

During the recording, execute the following. It reads the submitted project, uses the fresh environment and writes to a separate directory without overwriting frozen outputs:

```powershell
.\projects\project-1\.build\video-venv\Scripts\python.exe projects/project-1/run.py --all --output projects/project-1/.build/video-cold-output
```

The assistant's separate cold_run.py receipt proves a copied-project/new-venv reproduction. Your command above demonstrates your own fresh-environment execution and ownership; do not call the assistant's earlier log your recorded run. Preserve the actual console result and any first failure/resolution.

| Planned time | Exact screen and scroll/action | Evidence to point at |
|---|---|---|
| 0:00-0:25 | TabE, inputs.json **`"dso":75`**, then model.py **`b['ar']=`**. | One driver becomes AR through revenue*days/365; this enters operatingNWC and cash flow. |
| 0:25-0:55 | model.py **`delta_nwc=`**, **`fcff=nopat`**, then **`terminal=rows`**. | Show actual formulas, cash/equity checks, FCFF at WACC and terminal reinvestment. Avoid reading unrelated functions. |
| 0:55-1:20 | TabF, run command above. | Successful end-to-end execution and actual PASS15/15; if it fails, show/diagnose the failure rather than read the success line. |
| 1:20-1:50 | TabC, **Numerical validation**, panel **V1 Known answer and company arithmetic**. | Published training EV1,624.87 / price27.50 versus actual; year1 NOPAT+D&A-capex-deltaNWC=191,481.49M. These are arithmetic evidence, not a PASS banner. |
| 1:50-2:20 | TabC, **V2 Highest-risk failure evidence**. Optionally click through to validation-results.json/test code. | Financial-asset contamination creates false discounted investment; a deliberately unsupported cash deficit produces an explicit error. Passing the test means the bad input was rejected. |
| 2:20-2:55 | TabC, **V3 Changed input: prediction versus result**. | WACC13.90->14.90%, value$118.58->$108.38, unchanged watch/defer, and why the action threshold did not change. |
| 2:55-3:15 | Your completed locked record/addendum **if supplied**, otherwise TabC **V4 Evidence boundary**. | Actual prediction author/time/precommit plus result and decision effect. The existing assistant technical test is not a completed human lock. If an instructor exception applies, identify the revised designation accurately. |

Script:

<!-- SCRIPT2 -->
“I will show how one input reaches the valuation, then the evidence that the model handles important errors.

The base collection assumption is seventy-five days. In the forecast, revenue times collection days divided by three hundred sixty-five produces receivables. Receivables feed operating working capital; the change in working capital reduces operating cash flow and FCFF. Cash is calculated from the cash-flow statement, and equity rolls through retained income. Neither is a balancing plug.

FCFF starts with after-tax operating profit, adds depreciation and amortization, and subtracts operating capital spending and working-capital investment. In the first forecast year, the result is approximately one hundred ninety-one point five billion dollars. The terminal formula requires reinvestment for growth, and operating cash flows are discounted at WACC before the ownership bridge.

I am running the submitted project in a new environment without third-party packages. The console reports the observed result. That alone does not establish financial correctness, so here are numerical checks.

The course's published training case gives enterprise value of one thousand six hundred twenty-four point eight seven million dollars and twenty-seven dollars fifty per share. The engine reproduces those answers and all nine sensitivity cells within rounding tolerance.

The highest-risk diagnostic repeats the old mistake of scaling financial investments as operating assets. In that bounded calculation, it creates about one hundred twenty-six billion dollars of false discounted investment. This illustrates the danger; it is not a complete alternative valuation. A separate forced cash deficit is rejected with an explicit funding error. A passing failure test means the bad input was caught.

The changed-input result also has the expected direction: raising WACC from about thirteen-point-nine to fourteen-point-nine percent lowers value from one hundred eighteen dollars fifty-eight to one hundred eight dollars thirty-eight. Watch-defer remains because the market price still fails the entry threshold. That explains the unchanged action rather than pretending every sensitivity must reverse the decision.

The technical prediction and outcome are visible here. Any required human prediction timing and authorship must be supported by the separate actual record, rather than inferred from this retrospective explanation.”
<!-- /SCRIPT2 -->

If your completed record is available, replace the last paragraph with its actual committed prediction, timestamp, old/new units, predicted/actual direction and decision effect. Do not read guessed values. The local locked-changed-input-record.md currently says INCOMPLETE; a humanized retrospective draft is not an original pre-run artifact. Your reported in-class permission can change the permitted designation, but not the actual chronology.

## Video3 - defend the committee action

| Planned time | Exact screen and scroll/action | Decision evidence to show |
|---|---|---|
| 0:00-0:25 | TabH, memo **page1 / Committee ask and valuation range**. | No-position user,12-24month horizon, September10 date,218.36 price, causal range and conditional action. |
| 0:25-0:55 | TabG dashboard, **Enterprise to common equity**. | EV/equity/share bridge; investments counted once; debt and dilution. |
| 0:55-1:20 | Dashboard **WACC-growth sensitivity**; click the base-WACC/g3% row, then the WACC+1pp/g3% row. | Values$118.58 and$108.38, with same operating forecast. Current grid row5 and row8 excluding the header. Explain TVshare65.1% rather than imply precision. |
| 1:20-1:40 | TabH memo **page2 / Disagreement across methods**; TabC **C2 Method disagreement** if you need larger numbers. | Peer intervals, business/denominator differences and why no mechanical average. |
| 1:40-2:10 | Dashboard top, select **low**, then scroll to **Five rolling forecast years**, Income statement. | Low value$55.93/DO NOT INITIATE; show weaker operating results, not only a different dropdown label. The risk gate is an explicit adverse-regime policy, not proof from price alone. |
| 2:10-2:30 | Dashboard **Reverse DCF and conditions**, or TabC **C3 Market expectation**. | Market price requires +19.82pp in every DCgrowth assumption with all other base inputs fixed; not a unique market forecast. |
| 2:30-3:10 | TabH memo **page2 / Conditions, reversal triggers and next evidence**; TabC **C4 Committee monitoring** for the compact checklist. | Entrybelow$94.87 after refreshed evidence; report-by-report monitoring; two-quarter growth trigger, collection/margin risks and immediate review of material losses. Finish with the committee ask. |

Script:

<!-- SCRIPT3 -->
“For a fund with no current NVIDIA position and a twelve-to-twenty-four-month decision horizon, I recommend watch or defer. This is a September tenth, twenty-twenty-six valuation at a market price of two hundred eighteen dollars thirty-six, not a current quote.

The causal range is about fifty-six to two hundred twelve dollars per share, with a base reference near one hundred nineteen. These are different operating regimes, not confidence limits or precise price targets.

Here is how operating value reaches shareholders. The model adds separately valued cash and investments, subtracts debt and other claims, and divides common equity by the diluted-share proxy. It does not count financial investments again as operating working capital.

Base WACC is about thirteen-point-nine percent, and terminal growth is three percent with explicit reinvestment. Roughly sixty-five percent of enterprise value comes from the terminal period. The sensitivity grid therefore matters: adding one percentage point to WACC lowers value to about one hundred eight dollars even with the same operating forecast.

Peer references disagree with DCF. Historical P/E suggests about three hundred seventy-one to nine hundred thirty-one dollars, while EV-to-sales suggests about two hundred thirteen to two hundred fifty-two. Annual earnings lag current growth; AMD's margins and Broadcom's software mix differ from NVIDIA. Two qualified peers provide context, not a reason to average away the disagreement.

In the low case, deployments and financing slow, margins weaken and collections take longer. Additional supply losses and guarantee exposure produce a value near fifty-six dollars. We classify that adverse operating regime as do not initiate; the decision reflects the assumptions and risk policy, not simply a lower price estimate.

At fixed base assumptions, the market price requires roughly twenty additional percentage points of Data Center growth in every forecast year. That is one demanding conditional explanation, not proof the market is wrong.

I would consider initiation only below roughly ninety-five dollars using a refreshed base estimate and supported demand, margins and collections. Review each quarterly filing: two consecutive quarters of Data Center growth below twenty percent, collection days above ninety-five, gross margin below seventy percent, or material guarantee losses would challenge the thesis. The committee should keep NVIDIA on watch, refresh the evidence and require that price cushion before committing capital.”
<!-- /SCRIPT3 -->

## Evidence still needed and final handoff

Your statement that the labs/data are complete does not automatically update files saved elsewhere. In this local package, original checkpoint PDF/first receipt, completed human prediction timing record and confirmed partner attribution are still not present, and transcripts are pending. Use the completed actual records if you have them; do not spend video time reading blank placeholders as evidence. No script can prove an event without its artifact.

For the originally specified human lock, author the prediction with AI off before a new test, save old/new values/units and expected direction/action, commit it, then execute and append actual outcomes/diagnosis. If the instructor authorized a different AI-assisted exercise, record that permitted designation without claiming an AI-off event occurred. Never backdate an explanatory draft.

After recording, replace docs/transcript-video-1.txt through -3.txt with corrected actual speech and observed indices. Upload the three videos with stable accessible links. Update submission-manifest.csv with real titles/durations/access checks. Confirm speech, memo, visible output and validation agree. A later final-video freeze must use a new immutable tag; the recording-audit tag is not a completed-video submission. Submit the final bundle through Brightspace and retain its receipt; GitHub upload is separate. Check the assignment header for the enforced deadline/timezone.

## Final rehearsal check

For each scene, pause on a readable number or passage while making its claim. If you cannot point to evidence, remove or qualify the claim. Do not add invented sources, personally performed analyses, peer statements or completed events. If a live run fails, preserve the failure and diagnosis. Do not use “AI agrees” or “all tests pass” as a substitute for the specific source/arithmetic/failure evidence above. Keep the original videos and correct substantive transcript mistakes after recording.
