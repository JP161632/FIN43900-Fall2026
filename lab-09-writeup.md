# Lab 09 — ABG Integrated Pro Forma

## Decision question

What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?

The model estimates ABG's equity at **$291.75 per share**. The result is driven most strongly by three judgments: 1.8% annual organic revenue growth, a 17.05% gross margin, and SG&A declining from 66.5% to 64.5% of gross profit. Growth sets the sales base, gross margin converts sales to gross profit, and SG&A determines how much of that profit becomes operating income.

## Why cash is computed last

Cash is the balance sheet's residual outcome. The income statement must be completed first, followed by the non-cash balance-sheet accounts and financing flows. FCFE then captures the cash created or used by earnings, non-cash charges, investment, working capital, floor-plan borrowing, and debt repayment. Only after those flows and the buyback are known can ending cash and any required revolver draw or repayment be computed.

## Model checks

Each forecast year enforces two checks before valuation:

- Assets minus liabilities minus equity must round to 0.0.
- Cash must be at least the $25.0 million minimum after applying the revolver logic.

If FY2026 cash is incorrectly held at the opening $40.4 million instead of the computed $101.8 million, the balance-sheet check reports **FY2026E** and a **−$61.4 million** gap. That amount is the missing increase in cash, with the sign showing that assets are understated. The error therefore identifies both the affected year and the direction and size of the mistake before inspecting individual model lines.

## Floor-plan financing

Floor-plan financing consists of inventory loans provided by manufacturers' finance arms and banks. Because dealerships borrow to fund vehicles held for sale, the balance rises and falls with inventory. The model calculates interest on the opening floor-plan balance and treats the annual change in floor-plan borrowing as an operating component of FCFE. Removing the line eliminates a major source of inventory funding; ABG would have to finance the inventory itself, sending modeled cash to roughly negative $1.1 billion in the video example.

## Validation against the known answer

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |
| Value per share | $291.75 | — |

Approximately 80% of the estimated equity value comes from cash flows after 2030, so the valuation is especially sensitive to the cost of equity, terminal growth, and sustainable FCFE assumptions.

## Checkout files

- [`proforma.py`](proforma.py)
- [`lab-09-writeup.md`](lab-09-writeup.md)
