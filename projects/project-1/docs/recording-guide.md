# Student next steps - fixed-chart recording guide

**No tab tour. Use one fixed chart for each video.** Open `Recording-Charts.pdf`, choose the page for that video, and set the viewer to **Fit page** before recording. Stay on that page. Alternatively open the matching1920x1080PNG in an image viewer and fit the whole image to the window.

| Video | Exactly what to open | During the recording |
|---|---|---|
| 1 - Research evolution | Recording-Charts.pdf **page1**, or outputs/Video-1-Research-Chart.png | Stay on the same chart for the entire script. Move the cursor to the named boxes; no scrolling or opening sources. |
| 2 - Code and validation | Recording-Charts.pdf **page2**, or outputs/Video-2-Validation-Chart.png | Stay on the chart. Briefly bring a prepared terminal over it to execute the actual run, then minimize the terminal. No tabs or scrolling. |
| 3 - Committee defense | Recording-Charts.pdf **page3**, or outputs/Video-3-Committee-Chart.png | Stay on the same chart throughout. Point to the range line, method panel and trigger panel as you speak. |

The chart footer links point to the original lab, filing, code and executed outputs for grading. They do not need to be opened during Videos1/3. Detailed backup evidence remains in outputs/recording-proof.html and the submission PDFs. This chart is a condensed evidence surface, not a replacement for those submitted records.

## Before recording

Set screen recording to1920x1080 if possible. Fit the chart to the full screen and hide the PDF sidebar/browser controls. Keep this script on paper, a phone or a second display outside the recording area. Start recording only after the correct chart is visible. Webcam layout is a preference unless the instructor separately requires it. Keep audio clear and the chart legible.

Maximum3:00 for Video1; maximum5:00 each for Videos2/3. Aim about2:45-2:55 for Video1 and about3:00-3:30 for Videos2/3. Timings below are suggestions, not observed transcript indices. After recording, use actual timestamps and corrected actual speech in the transcripts.

## Video1 - one chart, research evolution

Question proved: **What changed or held after project-specific research, what drove it, and what evidence justified it?** The chart shows research admission -> earlier valuation -> correction/evidence -> revised valuation -> action held with conditions. It distinguishes the earlier sensitivity grid from the later causal range, and identifies course/prior-lab/AI/evidence contributions.

| Planned time | Stay on page1; point here | What it proves |
|---|---|---|
| 0:00-0:20 | Upper-left: **1 STARTING QUESTION** | Admission to research was not a buy recommendation. |
| 0:20-0:50 | Upper-middle: **2 EARLIER VALUATION / LAB5** | Earlier62.72base,55.59-72.40grid,WACC15.88%,annualweightedshares. |
| 0:50-1:15 | Lower-left: **WHAT CHANGED - AND WHY** | Prior lab limits and revised data/FCFF/method, not a claim every dollar came from one fix. |
| 1:15-1:40 | Lower-middle: **INDEPENDENT SOURCE CHECK** | Filing cash/debtsecurities56,586M versus equitysecurities42,783M; classification correction. |
| 1:40-2:20 | Upper-right revised valuation, then the note under the top row | Current$118.58base and$55.93-$212.08causal range; different method/range definitions and forecast windows. |
| 2:20-2:40 | Bottom **Source of change** band | Accurate contribution/attribution; facts/tests do not make forecast assumptions true. |
| 2:40-2:55 | Lower-right: **WHAT HELD / WHAT WOULD CHANGE** | Watch/defer held fromLab5; demand/collection/margin evidence and entrycondition govern action. |

Script:

<!-- SCRIPT1 -->
“My research began with a question, not a buy recommendation: could NVIDIA turn rapid Data Center growth into durable owner cash flows at a reasonable price? EditionA admitted NVIDIA for deeper research.

The first completed DCF, in Lab5, estimated sixty-two dollars and seventy-two cents per share. Its discount-rate and terminal-growth grid ran from about fifty-six to seventy-two dollars. It used the annual filing, a fifteen-point-eight-eight-percent WACC and annual weighted diluted shares. Its watch-defer conclusion was conditional, and the reverse-DCF search did not find a solution within its limited bracket.

The later labs exposed why I should not simply carry that number forward. Lab11 withheld a new valuation while investment classification, cash-flow labels and terminal assumptions remained unresolved. Those are finance problems that a balanced spreadsheet cannot rule out.

The independent filing check is summarized in the middle box. July cash and debt securities total fifty-six-point-six billion dollars, while marketable equity investments are a separate forty-two-point-eight billion. Financial holdings should not grow automatically as operating working capital, and unrealized investment gains are not operating cash generation.

The revised model uses a trailing operating base, five linked statements and an explicit ownership bridge. First-year FCFF is about one hundred ninety-one billion, versus one hundred thirty-one billion in Lab5, with different forecast windows. Its base reference is about one hundred nineteen dollars, with a causal range of fifty-six to two hundred twelve. That range is a set of different operating cases, not the same sensitivity interval as Lab5. The value change also reflects the reporting base, forecast, WACC, terminal reinvestment and share basis; I cannot assign it all to one correction.

Course requirements drove the FCFF architecture. Earlier labs recorded the limitations. AI assisted the rebuild and checks; filings and numerical tests support accepting or qualifying its output. Growth, discount-rate and investment-recovery choices remain assumptions to challenge.

The later watch-defer action held at the dated two-hundred-eighteen-dollar market price. What evolved was the evidence and the conditions for acting, not a claim that uncertainty disappeared.”
<!-- /SCRIPT1 -->

No need to click a source during this video: the named source/locator and the condensed evidence are visible, and original documents remain linked in the submitted files. Do not present the typeset EditionA summary as proof of an original checkpoint receipt or a fictional response as real partner evidence.

## Video2 - one chart plus a short actual-run overlay

Question proved: **How does submitted code produce the result, and what high-risk test passed or failed?** Page2 includes actual source excerpts, a driver/statement/FCFF/value chain, independent expected/actual numerical answers, a captured rejected input and the changed-input decision effect.

Prepare the terminal **before recording**, at the course repository root (FIN43900-Fall2026 folder). Create a fresh no-pip environment:

```powershell
.\.venv\Scripts\python.exe -m venv --without-pip projects/project-1/.build/video-venv
```

Have this command ready but do not execute it until the recording is running:

```powershell
.\projects\project-1\.build\video-venv\Scripts\python.exe projects/project-1/run.py --all --output projects/project-1/.build/video-cold-output
```

For the run, bring the terminal to the foreground over the chart, execute the command, hold the result long enough to read, then minimize it. This is a single short overlay, not a tab tour. Record the actual result; if it fails, preserve the first failure and diagnosis instead of reading a prepared success line. A static chart cannot prove your own live cold run. The assistant's separate copied-project cold-run receipt remains technical backup, not your recording.

| Planned time | Stay on page2; point/action | What it proves |
|---|---|---|
| 0:00-0:35 | Top driver-to-value row, left to right | DSO75 ->receivables ->operatingNWC/FCFF ->ownership value. |
| 0:35-1:05 | **Source excerpts + terminal math** strip | Actual model expressions, FCFF economics and growth reinvestment. |
| 1:05-1:25 | Brief terminal overlay; run command and minimize | Your actual fresh-environment execution and observed15-test result. |
| 1:25-1:55 | Lower-left: **KNOWN ANSWER** | Course answers1624.87EV/27.50share versus actual engine results, not just a PASS label. |
| 1:55-2:25 | Lower-right: **HIGH-RISK FAILURE EVIDENCE** | Forced cash deficit caught; classification diagnostic quantified and properly limited. |
| 2:25-2:55 | Lower-middle: **EXPECTED -> ACTUAL -> DECISION** | WACC+1pp,$118.58->$108.38,expectedlower/actuallower,watch/defer held for a threshold reason. |
| 2:55-3:15 | Bottom **Controls / Evidence boundary** | Accounting checks and honest distinction between technical tests and authentic prediction history. |

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

The source-code expressions and saved validation outcomes are on the chart. The original code, full numerical tests and cold-run log are linked below it for review; you do not need to open them while narrating. If the instructor specifically requests a separate code-editor demonstration, add it as required; this fixed-chart route does not claim to waive instructor requirements.

## Video3 - one chart, committee defense

Question proved: **What should the committee do, under what conditions, and what would reverse it?** A stationary committee chart is appropriate here: defend the decision rather than tour interface features.

| Planned time | Stay on page3; point here | What it proves |
|---|---|---|
| 0:00-0:30 | Title/date and upper valuation range | User/horizon/date,218.36market,conditionalwatch/defer and causal range. |
| 0:30-0:55 | Bottom **Ownership bridge** line | OperatingEV ->adjustments ->common equity /dilutedshares; no free investments. |
| 0:55-1:20 | **WHY THIS DCF NEEDS CAUTION** | WACC/g/ROIC,terminalshare65.1% and discount-rate sensitivity. |
| 1:20-1:50 | **WHY METHODS DISAGREE** | Peer references versusDCF; different denominators/mix; no mechanical average. |
| 1:50-2:15 | **Downside changes action** band | Causal operating/financing deterioration changes action under the declared riskpolicy. |
| 2:15-2:35 | Lower half of **WHY THIS DCF NEEDS CAUTION** | ReverseDCF marketexpectation is one conditional solution. |
| 2:35-3:15 | **WHAT WOULD REVERSE THE ACTION**, then entryceilingunder the range | Quarterly review,metric/window triggers and conditionalprice/evidence ask. |

Script:

<!-- SCRIPT3 -->
“For a fund with no current NVIDIA position and a twelve-to-twenty-four-month decision horizon, I recommend watch or defer. This is a September tenth, twenty-twenty-six valuation at a market price of two hundred eighteen dollars thirty-six, not a current quote.

The causal range is about fifty-six to two hundred twelve dollars per share, with a base reference near one hundred nineteen. These are different operating regimes, not confidence limits or precise price targets.

Here is how operating value reaches shareholders. The model adds separately valued cash and investments, subtracts debt and other claims, and divides common equity by the diluted-share proxy. It does not count financial investments again as operating working capital.

Base WACC is about thirteen-point-nine percent, and terminal growth is three percent with explicit reinvestment. Roughly sixty-five percent of enterprise value comes from the terminal period. The sensitivity test therefore matters: adding one percentage point to WACC lowers value to about one hundred eight dollars even with the same operating forecast.

Peer references disagree with DCF. Historical P/E suggests about three hundred seventy-one to nine hundred thirty-one dollars, while EV-to-sales suggests about two hundred thirteen to two hundred fifty-two. Annual earnings lag current growth; AMD's margins and Broadcom's software mix differ from NVIDIA. Two qualified peers provide context, not a reason to average away the disagreement.

In the low case, deployments and financing slow, margins weaken and collections take longer. Additional supply losses and guarantee exposure produce a value near fifty-six dollars. We classify that adverse operating regime as do not initiate; the decision reflects the assumptions and risk policy, not simply a lower price estimate.

At fixed base assumptions, the market price requires roughly twenty additional percentage points of Data Center growth in every forecast year. That is one demanding conditional explanation, not proof the market is wrong.

I would consider initiation only below roughly ninety-five dollars using a refreshed base estimate and supported demand, margins and collections. Review each quarterly filing: two consecutive quarters of Data Center growth below twenty percent, collection days above ninety-five, gross margin below seventy percent, or material guarantee losses would challenge the thesis. The committee should keep NVIDIA on watch, refresh the evidence and require that price cushion before committing capital.”
<!-- /SCRIPT3 -->

## After recording

Replace docs/transcript-video-1.txt through -3.txt with corrected **actual** speech and observed timestamps. Provide videoURLs,titles,durations and accesschecks for the finalmanifest and consistencyreview. Original videos are still required; charts/scripts do not count as recordings. A final-video freeze needs a new immutabletag and the Brightspace finalsubmission receipt.

Current evidence update: the student terminal-growth prediction is precommitted at5a9de1d and executed; g3%->2.5% gives $118.58->$116.57 with WATCH/DEFER unchanged. Attributed peer review is supplied. Original checkpointPDF/receipt and audio/timestamp verification remain open. See the locked record for actual author/executor timing and reported instructor wording permission. The scripts above remain preparation history, not transcripts of a new recording.
