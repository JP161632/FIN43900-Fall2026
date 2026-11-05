# Lab 19 — Rubric Review

The completed work covers the COST known answer, SMH's largest holding NVDA, checked memos, partner discussion and a conditional screening decision. All 23 calculation and memo checks and ten app checks pass.

| Criterion | Evidence | Current assessment |
|---|---|---|
| Known answer reproduced | [COST report](evidence/COST-report.md), [independent verifier](verify_lab19.py), [results](verification-results.json) | All ten ratios and eight checks match; calculated from saved SEC facts, not typed into production logic |
| Numbers in code | [Shared script](panel.py), [nine memos](memos), [app tests](app-verification-results.json) | All saved memo numbers occur in printed output; injection is caught in every investor's text in both helper and real app |
| Honest gaps | [JPM report](evidence/JPM-report.md), missing-input/denominator/history tests | Missing facts and unknown checks preserved; no estimates; sector limitations disclosed |
| Your company run | [NVDA report](evidence/NVDA-report.md), [three memos](memos/NVDA), [holding source check](evidence/SMH-holding-selection.md) | Buffett 3/3, Graham 3/3, Burry 1/2; real cash-backing failure retained and app output verified |
| The decision | [Writeup](lab-19-writeup.md) records the conditional screening decision | Use only as an initial negative screen with preserved unknowns, industry context and independent DCF; NVDA cash-backing failure explicitly triggers investigation |

The writeup includes the opening discussion, code explanation, missing-input question, role swaps, two-sentence bull and bear cases, and reflections on agreement and thresholds. The cases follow the computed NVDA results. Moat durability, customer concentration and working-capital efficiency remain research questions where the panel provides no evidence. Graham's retained threshold is 2.0.
