# Lab 19 — Legend Panel

**Status:** COST panel, investor skills, six printed-number-checked memos (COST plus the JPM gap probe), app and verification complete. The Project 2 fund/holding, personal decision and actual partner exchanges await student input. JPM is not claimed as the fund's largest holding.

## D — The question

When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

The same evidence can support different judgments because each investor emphasizes different risks. Buffett's assigned rules reward profitability and owner earnings, Graham demands liquidity plus positive/growing earnings, and Burry checks cash backing and leverage. The split can reflect a stated rule rather than a disagreement about facts. A panel merits conditional use as a transparent screen; its shared data and model can also produce shared errors.

**Opening discussion preparation, not an invented exchange:** Graham can reject COST under a strict liquidity hurdle even while Buffett's earning-power checks pass. Burry would question whether reported profits are supported by operating cash and what balance-sheet risks remain after his simple tests. The assigned [Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md) and [Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md) pages inform those perspectives; the lab defines the exact executable checks.

## Build — shared facts and distinct lenses

The AI-assisted [build request](request.md) preserves Lab 18's SEC engine and app and adds a companion [panel app](app.py). It retains the chart, complete facts, provenance, editable memos and number flag. The [Graham](../../.agents/skills/graham-edgar/SKILL.md), [Burry](../../.agents/skills/burry-edgar/SKILL.md) and extended [Buffett](../../.agents/skills/buffett-edgar/SKILL.md) skills direct each memo to use the same printed report.

The code selects facts and evaluates checks; the model writes each separate judgment after reading that output. The app displays saved model-written memos rather than generating fresh judgments automatically. These are three skill-guided perspectives from one assistant, not three independently sourced investigations or autonomous agent runs.

## V — COST known answer

The [printed report](evidence/COST-report.md) reproduces every assigned ratio. Raw facts are reused from Lab 18's November 3, 2026 SEC snapshot; replaying them is not a new retrieval. The code never imports the answer key as an input. Full tags, amounts, filing dates, accessions and the source hash accompany the output.

| Fiscal-year end | Current ratio | Liabilities/equity |
|---|---:|---:|
| 2022-08-28 | 1.02 | 2.11 |
| 2023-09-03 | 1.07 | 1.75 |
| 2024-09-01 | 0.97 | 1.96 |
| 2025-08-31 | 1.03 | 1.64 |
| 2026-08-30 | 1.06 | 1.49 |

| Investor | Check | COST |
|---|---|---|
| Buffett | ROE at least 15% every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first to last | pass |
| Graham | Current ratio at least 2.0, latest year | fail: 1.06 |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass: 1.49 |

Buffett passes **3 of 3**, Graham **2 of 3**, Burry **2 of 2**. The [independent audit](verification-results.json) confirms the ten ratios and eight check outcomes. Twenty source/calculation/memo checks and nine [app checks](app-verification-results.json) pass. Injection into each investor's memo produces an investor-specific unsupported-number flag; reloading clears the unsaved edit. All six saved memos have no unsupported numeric tokens and were also read for correct attribution.

**Investor judgments:** [Buffett](memos/COST/buffett.md) says watch it because consistent returns warrant further investigation of durability. [Graham](memos/COST/graham.md) passes on the strict defensive screen because liquidity fails. [Burry](memos/COST/burry.md) says watch it with the assigned accounting checks passing, while reserving judgment about footnotes and hidden risks. A quantitative pass count is distinct from an investment verdict.

## Probe — threshold as policy

The [temporary-threshold report](evidence/COST-probe-report.md) runs identical facts at a 1.0 Graham hurdle. Graham becomes **3 of 3**; Buffett and Burry are unchanged. The retained skill setting remains **2.0**. The probe was executed through the explicit CLI override and the actual app checkbox; the original saved setting was preserved.

**Proposed threshold choice, awaiting student confirmation:** Keep 2.0 to preserve the assigned defensive liquidity cushion and comparability across companies rather than selecting a hurdle after observing COST. This line also appears under Graham's memo. A threshold can change a verdict without changing the business, so it must be stated and justified before relying on a screen.

## Your company — confirmation pending

The student has been asked for the Project 2 fund, holdings date/source and largest-company ticker. No holding is assumed. If that company lacks an eligible 10-K, the next-largest qualifying company must be identified and the substitution explained. Its panel, three judgments, memos, gaps and discussion will be added after confirmation.

**Additional gap probe:** [JPM's printed panel](evidence/JPM-report.md) preserves missing capital spending and owner earnings, and its current-assets/current-liabilities tags are not found throughout. Graham's current ratio stays not known; the earnings checks pass. Buffett has a failed ROE check and two unknown owner-earnings checks; Burry fails both checks. These results show honest gaps and the need for sector-specific interpretation. They do not satisfy the unconfirmed fund-holding requirement.

## Explain the code — preparation for the no-AI exercise

Open `graham_checks` in [panel.py](panel.py). Read it line by line:

1. The function receives the selected annual rows and the current-ratio hurdle.
2. It takes the last row's computed current ratio, or `None` if no rows exist. The ratio helper already returns `None` when either input is absent or current liabilities are nonpositive.
3. It collects each row's net income, preserving `None` for missing facts.
4. It records whether exactly five annual rows exist.
5. The liquidity entry calls `check` with the latest ratio and an inclusive `>=` predicate.
6. The positive-income entry requires complete history and all incomes strictly positive.
7. The growth entry requires complete inputs for the whole history, then compares final with first income using strict `>`.
8. It returns the mapping of readable check names to pass, fail or not known.

The shared `check` helper first tests completeness and missing inputs. If either fails, it returns `not known` before evaluating the predicate; otherwise it returns pass or fail. Missing data therefore never silently becomes zero or a failed screen. A one-row history can support a latest-year check while its annual checks remain unknown. An interior missing income makes both annual Graham checks unknown even if their endpoints exist.

**Partner missing-input question to practice:** What if latest current liabilities are absent? The raw amount prints not found, the ratio helper returns `None`, and the liquidity check returns not known. No division or guessed denominator occurs.

**Actual partner exercise:** Pending the student's account of the explanation, question/answer and role swap. Preparation above is not a claim that a no-AI exchange occurred.

## Bull and bear — awaiting the confirmed company

The required two-sentence bull case and two-sentence partner bear case must use the same confirmed company panel. They remain pending rather than being attributed to a partner who has not supplied them. The student has been prompted for the actual exchange and swap.

## Your decision

**Proposed one-line decision for student review:** Only with a condition: use the panel to prioritize research after checking the filings, preserving every unknown and fixing thresholds in advance; require sector context and independent business/valuation work before selecting a Project 2 investment.

**Student's own decision:** Pending response. The proposal above is an AI draft, not an attributed student choice.

## Learn on your own — a panel of AI agents

A panel brings multiple roles or analytical lenses to a common problem and compares their conclusions. In a full agent system, a coordinator can give each role its instructions and tools, then collect their independent runs for review. This lab implements the roles as reusable skills, deterministic checks and separately written memos shown together.

The personas disagree because the objectives and rules differ: earning power, liquidity protection and accounting skepticism ask different questions of identical facts. The code makes those differences visible; the memo explains the judgment. More personas do not create more independent evidence when they share a source, selector and model. Agreement can reflect a shared blind spot, and a majority vote cannot repair a missing input.

**Partner teaching and reflection:** Pending the student's report. Explain where the confirmed company's panel agrees and splits, then connect the threshold probe to the distinction between a financial fact and a screening-policy choice. The no-AI activities and quiz checkout have not been claimed as completed.
