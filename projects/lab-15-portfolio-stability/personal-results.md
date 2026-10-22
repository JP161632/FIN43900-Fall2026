# Personal portfolio results

Reproduce offline with `python analyze_personal.py`. All calculations import the same `portfolio.py` used by the app.

Historical annualized arithmetic estimates, gross of fees, not forecasts. Objective 10.00%; reserve minimum 0.00%. Weight order: NVDA / MSFT / TSM / QCOM.

| Run | Weights (%) | Return (%) | Volatility (%) | Reserve (%) |
|---|---|---:|---:|---:|
| all_months | 0 / 70 / 25 / 5 | 21.55 | 24.82 | 0.00 |
| last_36 | 0 / 55 / 45 / 0 | 39.62 | 21.69 | 0.00 |
| TSM_minus_1_point | 0 / 70 / 25 / 5 | 21.30 | 24.82 | 0.00 |

Largest window weight change: **20.00 points**.

TSM attack: 36.52% → 35.52%; largest weight change **0.00 points**.

The return floor is nonbinding: every asset's all-month historical estimate exceeds 10%, including TSM after its one-point cut. Changing only that mean leaves the covariance-based minimum-risk mix feasible and unchanged. Window estimation changes volatilities and correlations as well as means, producing the 20-point TSM weight change.

## Estimated inputs

| Asset | All-month return (%) | All-month volatility (%) | Last-36 return (%) | Last-36 volatility (%) |
|---|---:|---:|---:|---:|
| NVDA | 61.11 | 50.09 | 62.96 | 37.22 |
| MSFT | 16.43 | 27.31 | 20.91 | 28.49 |
| TSM | 36.52 | 36.78 | 62.48 | 30.77 |
| QCOM | 18.48 | 44.81 | 29.27 | 47.41 |

## Correlations — All 60 monthly returns

| Asset | NVDA | MSFT | TSM | QCOM |
|---|---:|---:|---:|---:|
| NVDA | 1.0000 | 0.6136 | 0.6051 | 0.4860 |
| MSFT | 0.6136 | 1.0000 | 0.3115 | 0.3844 |
| TSM | 0.6051 | 0.3115 | 1.0000 | 0.4456 |
| QCOM | 0.4860 | 0.3844 | 0.4456 | 1.0000 |

## Correlations — Last 36 monthly returns

| Asset | NVDA | MSFT | TSM | QCOM |
|---|---:|---:|---:|---:|
| NVDA | 1.0000 | 0.5278 | 0.5205 | 0.4030 |
| MSFT | 0.5278 | 1.0000 | 0.0769 | 0.3788 |
| TSM | 0.5205 | 0.0769 | 1.0000 | 0.3595 |
| QCOM | 0.4030 | 0.3788 | 0.3595 | 1.0000 |
