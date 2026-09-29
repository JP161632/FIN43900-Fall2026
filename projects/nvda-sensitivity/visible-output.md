# NVDA sensitivity: visible output

Units: USD millions. Final forecast year: FY2031E.

FCFE = modeled free cash flow to equity before dividends/buybacks.

Unavailable: Lab 10 discounts cash after dividends/buybacks and filters negative cash flows. Other assets also combine operating assets and marketable securities. Valuation needs reconciliation; no terminal value or per-share value is generated here. FCFE below is before shareholder payouts, under the inherited aggregate reinvestment convention.

| Run | Operating profit | Signed change | FCFE | Signed change | Checks |
|---|---:|---:|---:|---:|---|
| Base before | 331,370.934759 | +0.000000 | 242,008.189247 | +0.000000 | PASS |
| REVENUE_GROWTH / lower | 267,645.754998 | -63,725.179761 | 208,417.187134 | -33,591.002113 | PASS |
| REVENUE_GROWTH / base | 331,370.934759 | +0.000000 | 242,008.189247 | +0.000000 | PASS |
| REVENUE_GROWTH / higher | 406,682.510841 | +75,311.576082 | 279,077.113521 | +37,068.924274 | PASS |
| GROSS_MARGIN / lower | 321,037.232566 | -10,333.702193 | 233,055.242587 | -8,952.946660 | PASS |
| GROSS_MARGIN / base | 331,370.934759 | +0.000000 | 242,008.189247 | +0.000000 | PASS |
| GROSS_MARGIN / higher | 341,704.636952 | +10,333.702193 | 250,961.135907 | +8,952.946660 | PASS |

## Actual ranges and units

```json
[
  {
    "input": "REVENUE_GROWTH",
    "units": "decimal fraction of prior-year revenue; endpoints shift base by minus/plus 5 percentage points in each FY2027-FY2031",
    "reason": "Judgment: test a sustained faster or slower growth fade while preserving the existing declining path. Five percentage points each year creates a meaningful compounding test without extending recent historical growth rates. Endpoints are scenarios, not confidence bounds.",
    "lower": {
      "2027": 0.25,
      "2028": 0.2,
      "2029": 0.15,
      "2030": 0.1,
      "2031": 0.05
    },
    "base": {
      "2027": 0.3,
      "2028": 0.25,
      "2029": 0.2,
      "2030": 0.15,
      "2031": 0.1
    },
    "higher": {
      "2027": 0.35,
      "2028": 0.3,
      "2029": 0.25,
      "2030": 0.2,
      "2031": 0.15
    }
  },
  {
    "input": "GROSS_MARGIN",
    "units": "decimal fraction of current-year revenue; endpoints shift base by minus/plus 2 percentage points in each FY2027-FY2031",
    "reason": "Judgment: a two-percentage-point deviation tests weaker or stronger gross profitability while leaving the base recovery shape intact. It is a moderate variation relative to the filed FY2025 75.0% and FY2026 71.1% gross margins, not a statistically estimated interval.",
    "lower": {
      "2027": 0.7,
      "2028": 0.705,
      "2029": 0.71,
      "2030": 0.71,
      "2031": 0.71
    },
    "base": {
      "2027": 0.72,
      "2028": 0.725,
      "2029": 0.73,
      "2030": 0.73,
      "2031": 0.73
    },
    "higher": {
      "2027": 0.74,
      "2028": 0.745,
      "2029": 0.75,
      "2030": 0.75,
      "2031": 0.75
    }
  }
]
```

## Output spans over these ranges

Maximum minus minimum across valid runs only; incomplete groups are not ranked.
```json
[
  {
    "driver": "REVENUE_GROWTH",
    "valid_runs": 3,
    "operating_profit": 139036.75584300002,
    "fcfe": 70659.92638678529
  },
  {
    "driver": "GROSS_MARGIN",
    "valid_runs": 3,
    "operating_profit": 20667.40438620001,
    "fcfe": 17905.893319286522
  }
]
```

Restored base: PASS; maximum statement difference = 0.000000000 USD million; tolerance = 1e-06 USD million. Inputs identical: True.

## All annual checks

### base_before
- FY2027: PASS; cash 86,433.667510 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": 0.0}
- FY2028: PASS; cash 195,926.874401 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 1.4551915228366852e-11, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": -2.9103830456733704e-11}
- FY2029: PASS; cash 343,632.050372 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": -2.9103830456733704e-11, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": 0.0}
- FY2030: PASS; cash 528,935.367246 >= 10,000.000000; residuals {"balance_sheet": -1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 5.820766091346741e-11, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 749,969.556493 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 5.820766091346741e-11}
### REVENUE_GROWTH / lower
- FY2027: PASS; cash 88,341.146029 >= 10,000.000000; residuals {"balance_sheet": 5.820766091346741e-11, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 4.547473508864641e-13, "equity_rollforward": 0.0}
- FY2028: PASS; cash 195,165.168320 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 0.0}
- FY2029: PASS; cash 332,674.463640 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 2.7284841053187847e-12, "equity_rollforward": 0.0}
- FY2030: PASS; cash 497,426.339590 >= 10,000.000000; residuals {"balance_sheet": -1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -9.094947017729282e-13, "equity_rollforward": 5.820766091346741e-11}
- FY2031: PASS; cash 684,869.526724 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": -5.820766091346741e-11, "ppe_rollforward": 2.7284841053187847e-12, "equity_rollforward": 0.0}
### REVENUE_GROWTH / base
- FY2027: PASS; cash 86,433.667510 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": 0.0}
- FY2028: PASS; cash 195,926.874401 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 1.4551915228366852e-11, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": -2.9103830456733704e-11}
- FY2029: PASS; cash 343,632.050372 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": -2.9103830456733704e-11, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": 0.0}
- FY2030: PASS; cash 528,935.367246 >= 10,000.000000; residuals {"balance_sheet": -1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 5.820766091346741e-11, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 749,969.556493 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 5.820766091346741e-11}
### REVENUE_GROWTH / higher
- FY2027: PASS; cash 84,526.188991 >= 10,000.000000; residuals {"balance_sheet": -5.820766091346741e-11, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -4.547473508864641e-13, "equity_rollforward": 2.9103830456733704e-11}
- FY2028: PASS; cash 196,503.279716 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": -2.9103830456733704e-11}
- FY2029: PASS; cash 354,459.054120 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": -5.820766091346741e-11}
- FY2030: PASS; cash 561,431.764888 >= 10,000.000000; residuals {"balance_sheet": 2.3283064365386963e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": -5.820766091346741e-11, "ppe_rollforward": -5.4569682106375694e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 819,534.878409 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -3.637978807091713e-12, "equity_rollforward": 0.0}
### GROSS_MARGIN / lower
- FY2027: PASS; cash 80,768.696950 >= 10,000.000000; residuals {"balance_sheet": -5.820766091346741e-11, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": 2.9103830456733704e-11}
- FY2028: PASS; cash 184,222.044252 >= 10,000.000000; residuals {"balance_sheet": -5.820766091346741e-11, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": 0.0}
- FY2029: PASS; cash 324,731.456397 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": -2.9103830456733704e-11}
- FY2030: PASS; cash 501,824.729469 >= 10,000.000000; residuals {"balance_sheet": 1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 713,905.972057 >= 10,000.000000; residuals {"balance_sheet": -2.3283064365386963e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 1.1641532182693481e-10}
### GROSS_MARGIN / base
- FY2027: PASS; cash 86,433.667510 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": 0.0}
- FY2028: PASS; cash 195,926.874401 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 1.4551915228366852e-11, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": -2.9103830456733704e-11}
- FY2029: PASS; cash 343,632.050372 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": -2.9103830456733704e-11, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": 0.0}
- FY2030: PASS; cash 528,935.367246 >= 10,000.000000; residuals {"balance_sheet": -1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 5.820766091346741e-11, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 749,969.556493 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 5.820766091346741e-11}
### GROSS_MARGIN / higher
- FY2027: PASS; cash 92,098.638069 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": -2.9103830456733704e-11}
- FY2028: PASS; cash 207,631.704550 >= 10,000.000000; residuals {"balance_sheet": 1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": 0.0}
- FY2029: PASS; cash 362,532.644348 >= 10,000.000000; residuals {"balance_sheet": 1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": -2.9103830456733704e-11}
- FY2030: PASS; cash 556,046.005022 >= 10,000.000000; residuals {"balance_sheet": 1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": -5.820766091346741e-11, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 5.820766091346741e-11}
- FY2031: PASS; cash 786,033.140929 >= 10,000.000000; residuals {"balance_sheet": 2.3283064365386963e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 5.820766091346741e-11, "ppe_rollforward": 0.0, "equity_rollforward": -1.1641532182693481e-10}
### base_after
- FY2027: PASS; cash 86,433.667510 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": -1.3642420526593924e-12, "equity_rollforward": 0.0}
- FY2028: PASS; cash 195,926.874401 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 1.4551915228366852e-11, "ppe_rollforward": 9.094947017729282e-13, "equity_rollforward": -2.9103830456733704e-11}
- FY2029: PASS; cash 343,632.050372 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": -2.9103830456733704e-11, "ppe_rollforward": -1.8189894035458565e-12, "equity_rollforward": 0.0}
- FY2030: PASS; cash 528,935.367246 >= 10,000.000000; residuals {"balance_sheet": -1.1641532182693481e-10, "cash_rollforward": 0.0, "fcfe_payout_bridge": 5.820766091346741e-11, "ppe_rollforward": 3.637978807091713e-12, "equity_rollforward": 0.0}
- FY2031: PASS; cash 749,969.556493 >= 10,000.000000; residuals {"balance_sheet": 0.0, "cash_rollforward": 0.0, "fcfe_payout_bridge": 0.0, "ppe_rollforward": 0.0, "equity_rollforward": 5.820766091346741e-11}

Full annual statements and independent inputs for every run: results.json.
