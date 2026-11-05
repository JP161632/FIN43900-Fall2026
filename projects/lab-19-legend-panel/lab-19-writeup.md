# Lab 19 — Legend Panel

**Status:** COST panel, investor skills, six printed-number-checked memos (COST plus the JPM gap probe), app and verification complete. The student supplied SMH/NVDA, the retained threshold, decision and partner exchanges. NVDA's SEC download and panel remain pending the required runtime contact; its exact check results are not assumed. JPM is only an extra gap probe.

## D — The question

When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

The same evidence can support different judgments because each investor emphasizes different risks. Buffett's assigned rules reward profitability and owner earnings, Graham demands liquidity plus positive/growing earnings, and Burry checks cash backing and leverage. The split can reflect a stated rule rather than a disagreement about facts. A panel merits conditional use as a transparent screen; its shared data and model can also produce shared errors.

**Opening discussion — student-reported:** I explained that Buffett's earning-power checks pass COST, while Graham's current ratio of 1.06 falls below the defensive hurdle of 2.0. Burry's assigned checks pass because operating cash flow meets or exceeds net income in every selected year and latest liabilities/equity is 1.49. When we swapped, my partner described Graham's focus on liquidation protection and financing buffers and Burry's skepticism toward revenue recognition and hidden obligations. The assigned [Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md) and [Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md) pages inform those lenses; the lab defines the exact executable checks. The leverage pass applies to the latest year, not the entire history: COST's earliest printed ratio is 2.11.

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

**Student's threshold choice:** Keep 2.0. Lowering the hurdle after seeing COST's result would move the goalposts; keeping the assigned liquidity cushion preserves a consistent screening policy across companies. This choice also appears under Graham's memo. A threshold can change a verdict without changing the business, so it must be stated and justified before relying on a screen.

## Your company — NVIDIA in SMH

The student selected **VanEck Semiconductor ETF (SMH)** and its largest holding, **NVIDIA (NVDA)**. The student reports roughly 20% weight and cites the September 30, 2026 issuer holdings and SEC Form N-PORT. That exact month-end weight and N-PORT accession have not been independently reproduced; they are not inputs to the company screen. The [official VanEck page](https://www.vaneck.com/us/en/investments/semiconductor-etf-smh?redirectVE=generic), read November 5, lists NVDA as largest at **20.46% as of November 4, 2026**. The [selection note](evidence/SMH-holding-selection.md) keeps those dates distinct. NVIDIA files 10-Ks, so no next-largest-company substitution is needed. The SEC companyfacts download and panel execution await the runtime SEC contact requested from the student.

**Additional gap probe:** [JPM's printed panel](evidence/JPM-report.md) preserves missing capital spending and owner earnings, and its current-assets/current-liabilities tags are not found throughout. Graham's current ratio stays not known; the earnings checks pass. Buffett has a failed ROE check and two unknown owner-earnings checks; Burry fails both checks. These results show honest gaps and the need for sector-specific interpretation. JPM is an extra probe, not the selected fund holding.

## Explain the code — student-reported no-AI exercise

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

**Partner question and student's answer:** My partner asked what happens if latest current liabilities are missing from a company's 10-K. I answered that the ratio helper returns `None` and the shared check returns not known without guessing or dividing by zero. More precisely, the raw liabilities cell prints **not found**, while the derived current ratio prints **not known**. The ratio helper does not label the missing ratio not found.

**Actual exchange — student-reported:** I explained `graham_checks` line by line without AI: latest liquidity against the hurdle, positive income across five years, endpoint growth and the helper's missing-input guard. On the role swap, my partner explained `burry_checks`. I asked what happens when operating cash flow is below net income in just one year; my partner answered that the every-year cash-backing check fails. This is correct when all required inputs are present. If any required input is missing, this implementation returns not known before evaluating comparisons. Passing this consistency check supports cash backing but does not prove all profits are free of accounting manipulation.

## Bull and bear — student-reported exchange, evidence check pending

**Student's reported bull position:** Strong ROE, cash backing and earnings growth favor further research into NVIDIA's franchise. The submitted explanation also asserted large cash reserves and an unmatched competitive moat; these are not established by the assigned panel, and no unsupported cash-reserve figure or moat conclusion is adopted.

**Partner's reported bear position:** Rapid expansion may expose the business to inventory, receivable and funding pressures, while concentrated customer demand may make earnings sensitive to data-center spending. Those are hypotheses to investigate; the panel does not contain turnover, customer concentration or supply-chain evidence. The supplied claim about more than 40% of sales going to four hyperscalers is omitted because it is outside the printed facts and lacks a verified source in this lab. The final two-sentence cases will use NVDA's actual computed panel rather than assume that Graham or Burry fails it.

**Role swap — student-reported:** We immediately swapped bull and bear roles to defend the opposing sides. These activity descriptions are supplied by the student; the assistant did not observe the exchange.

**Company reflection awaiting the run:** The submitted reflection described agreement on genuine cash earnings and a split over valuation, peak earnings and customer concentration. The assigned checks cannot prove clean accounting, measure stock valuation or quantify customer concentration. Agreement and disagreement will be reported from the actual NVDA check results, with broader qualitative risks identified as open research questions.

## Your decision

**Student decision:** Only with a condition: use the panel as an initial negative screen to flag accounting or balance-sheet concerns, preserve unknowns for review, and require industry-specific context plus an independent discounted cash flow valuation before allocating capital.

A failed check is an investigation flag rather than proof of an accounting red flag; an unknown cannot be treated as a clean bill of health. This condition limits what the panel is allowed to decide and preserves the student's intended screening role.

## Learn on your own — a panel of AI agents

A panel brings multiple roles or analytical lenses to a common problem and compares their conclusions. In a full agent system, a coordinator can give each role its instructions and tools, then collect their independent runs for review. This lab implements the roles as reusable skills, deterministic checks and separately written memos shown together.

The personas disagree because the objectives and rules differ: earning power, liquidity protection and accounting skepticism ask different questions of identical facts. The code makes those differences visible; the memo explains the judgment. More personas do not create more independent evidence when they share a source, selector and model. Agreement can reflect a shared blind spot, and a majority vote cannot repair a missing input.

**Partner teaching — student-reported:** I explained that the same reported 10-K facts can yield different judgments because the personas emphasize earning power, defensive liquidity or cash-backing/leverage risk. I emphasized that unanimous agreement is not foolproof if the underlying SEC-reported data contains flaws. A filing's reported values and a panel's successful checks do not independently establish every accounting judgment as correct.

**Threshold reflection, edited for accuracy:** COST moving from failure at 2.0 to pass at 1.0 demonstrates that a screen's conclusion depends on policy thresholds as well as company facts. The business did not change during the probe. Sector and operating-cycle context may justify a different hurdle, but a ratio near 1.0 alone does not prove healthy liquidity, rapid turnover or a negative-working-capital model. COST's latest printed current ratio exceeds 1.0, so latest current assets exceed current liabilities; the supplied negative-working-capital claim is not supported for that period. Keep the threshold explicit and investigate the operating model before interpreting the verdict.

**Brightspace:** Quiz completion has not been reported and is not claimed here.
