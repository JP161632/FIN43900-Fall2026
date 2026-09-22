# Lab 09 - ABG Integrated Pro Forma

## Decision question and answer

**What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?**

The five-year ABG model estimates equity value of **$5,237.34 million**, or **$291.75 per share**. The statements are supported by an explicit assumption set, an integrated income statement, balance sheet, and cash flow statement, and automated checks that stop valuation if the balance sheet does not balance or cash falls below the required minimum.

## The three value-carrying judgments

1. **Organic revenue growth: 1.8% annually.** Growth determines the sales base on which profit and working-capital needs are calculated.
2. **Gross margin: 17.05%.** Gross margin converts sales into gross profit and therefore has a direct effect on operating income.
3. **SG&A as a share of gross profit: 66.5%, 65.5%, 64.5%, 64.5%, and 64.5%.** The assumed efficiency improvement determines how much gross profit reaches operating income.

These are judgments rather than mechanically observed facts, so they carry much of the valuation result and require a defensible business rationale.

## Assumption set

All currency amounts are USD millions unless stated otherwise.

| Assumption | ABG value | Label |
|---|---:|---|
| Organic revenue growth | 1.8% a year | Judgment |
| Gross margin | 17.05% | Judgment |
| SG&A / gross profit, 2026-2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | History |
| Impairment, non-cash | 120 a year | Judgment |
| Capital spending | 250 a year | Guidance |
| Tax rate | 25.5% | Judgment |
| Inventory days | 2,135.8 / (17,999.0 - 3,071.7) x 365 | History |
| Floor plan / inventory | 2,027.0 / 2,135.8 | History |
| Other working capital | 0.8% of the change in revenue | Judgment |
| Minimum cash / revolver limit / revolver rate | 25 / 850 / 6% | History / judgment / judgment |
| Debt repayment / share buyback | 150 / 150 a year | Judgment |
| Floor-plan / term-debt interest | 4.67% / 5.44% | History |
| Cost of equity / terminal growth | 10% / 2.5% | Judgment |
| Shares outstanding | 17.951349 million | Fact (10-Q, June 30, 2026) |

## Opening balance sheet - FY2025

| Account | Amount |
|---|---:|
| Revenue | 17,999.0 |
| Inventory | 2,135.8 |
| PP&E | 3,070.4 |
| Other assets | 6,371.6 |
| Cash | 40.4 |
| Floor plan | 2,027.0 |
| Term debt | 3,572.0 |
| Other liabilities | 2,127.5 |
| Equity | 3,891.7 |

Opening assets and liabilities plus equity both equal 11,618.2.

## Why cash is computed last

Cash is the balance sheet's residual outcome. The model first completes the income statement, then projects every non-cash balance-sheet account. FCFE captures the cash created or used by earnings, non-cash charges, capital spending, inventory, other working capital, floor-plan borrowing, and term-debt repayment. The model can only compute ending cash after these flows and the share buyback are known. It then draws the revolver if cash would be below $25 million or repays an opening revolver balance first when excess cash is available.

## Floor-plan financing

1. **What it is:** Floor-plan financing consists of inventory loans from manufacturers' finance arms and banks.
2. **How it works:** The loan balance rises and falls with inventory. Interest is calculated on the opening balance, and the change in the floor-plan balance is included in FCFE as an operating source or use of cash.
3. **Why removing it drives cash toward negative $1.1 billion:** Vehicle inventory still has to be purchased, but without floor-plan borrowing the matching source of cash disappears. ABG would have to fund the inventory itself, producing the large cash shortfall shown in the video.

## Checks and the meaning of the -61.4 error

Before valuation, `assert_balanced` checks every forecast year:

- Assets minus liabilities minus equity must round to 0.0.
- Ending cash must be at least the $25.0 million minimum after revolver activity.

If FY2026 cash is incorrectly held at the opening $40.4 million instead of the computed $101.8 million, the program refuses to value the company and reports `FY2026E balance-sheet gap: -61.4`. The amount is the omitted $61.4 million increase in cash, and the negative sign says assets are understated. It identifies the year, direction, and size of the error before opening a single model cell.

## Known-answer validation

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets - liabilities - equity | 0.0 | 0.0 |
| Value per share | $291.75 | - |

The present value of cash flows after 2030 is **79.8%** of total equity value, approximately the expected 80%. This concentration also shows why the valuation is especially sensitive to the cost of equity, terminal growth, and sustainable FCFE.

## Run instructions

From the repository root, run:

```text
python proforma.py
```

If `python` is not available on the terminal PATH, use the existing Windows virtual environment:

```text
.\.venv\Scripts\python.exe proforma.py
```

The file uses only the Python standard library.

## GitHub checkout links

- [proforma.py](https://github.com/JP161632/FIN43900-Fall2026/blob/main/proforma.py)
- [lab-09-writeup.md](https://github.com/JP161632/FIN43900-Fall2026/blob/main/lab-09-writeup.md)
