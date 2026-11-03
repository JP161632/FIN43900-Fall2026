"""Exercise the actual Streamlit page using archived SEC data, without network calls."""
import io
import json
from pathlib import Path

import pyarrow.ipc as ipc
from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parent


def run():
    checks = {}
    app = AppTest.from_file(str(HERE / "app.py"), default_timeout=30).run()
    checks["COST_table_checks_memo_and_notice"] = (
        not app.exception and not app.error and len(app.dataframe[0].value) == 5
        and list(app.table[0].value["Result"]) == ["pass", "pass", "pass"]
        and "not investment advice" in app.caption[0].value
        and "Verdict: watch it" in app.text_area[0].value
    )
    chart = app.get("vega_lite_chart")[0].proto
    dataset = ipc.open_stream(io.BytesIO(chart.datasets[0].data.data)).read_all().to_pandas()
    colors = dataset["color -- streamlit-generated"]
    owners = dataset[colors == "Owner earnings"].set_index("Fiscal-year end")["value -- streamlit-generated"]
    income = dataset[colors == "Net income"].set_index("Fiscal-year end")["value -- streamlit-generated"]
    checks["COST_chart_both_series_correct_endpoints"] = (
        len(owners) == len(income) == 5
        and owners["2022-08-28"] == 3501 and owners["2026-08-30"] == 9382
        and income["2022-08-28"] == 5844 and income["2026-08-30"] == 9226
    )
    original = app.text_area[0].value
    app.text_area[0].set_value(original + "\nHand-entered ROE: 40.0%.").run()
    injected_flag = any("40.0%" in item.value for item in app.error)
    app.button[0].click().run()  # Reload memo from file, discarding the injected edit.
    checks["hand_entered_number_flagged_then_reload_clears"] = injected_flag and not app.error and app.text_area[0].value == original
    app.sidebar.text_input[0].set_value("JPM").run()
    jpm_table = app.dataframe[0].value
    checks["JPM_gaps_checks_and_memo_visible"] = (
        not app.exception and not app.error
        and set(jpm_table["capital_spending"]) == {"not found"}
        and set(jpm_table["owner_earnings"]) == {"not found"}
        and list(app.table[0].value["Result"]) == ["fail", "not known", "not known"]
        and "cannot judge owner earnings" in app.text_area[0].value
        and any("not plotted as zero" in item.value for item in app.warning)
    )
    app.sidebar.text_input[0].set_value("../../COST").run()
    checks["invalid_ticker_isolated_without_exception"] = not app.exception and any("valid SEC ticker" in e.value for e in app.error)
    app.sidebar.text_input[0].set_value("ZZLAB").run()
    checks["unknown_ticker_error_without_fabricated_table"] = not app.exception and bool(app.error) and not app.dataframe
    checks = {name: bool(passed) for name, passed in checks.items()}
    result = {"method": "Streamlit AppTest with real archived SEC responses; no live network or browser screenshot", "checks": checks}
    (HERE / "app-verification-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return all(checks.values())


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
