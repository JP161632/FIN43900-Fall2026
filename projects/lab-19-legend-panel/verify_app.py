"""Exercise actual Streamlit outputs and interactions against preserved SEC responses."""
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parent


def run():
    checks = {}
    app = AppTest.from_file(str(HERE / "app.py"), default_timeout=30).run()
    checks["COST_table_ratios_and_eight_checks"] = (
        not app.exception and not app.error and len(app.dataframe[0].value) == 5
        and app.dataframe[0].value.iloc[-1]["current_ratio"] == "1.06"
        and app.dataframe[0].value.iloc[-1]["liabilities_to_equity"] == "1.49"
        and list(app.table[0].value["Result"]) == ["pass", "pass", "pass", "fail", "pass", "pass", "pass", "pass"])
    checks["three_memos_in_three_columns_with_verdicts"] = len(app.text_area) == 3 and len(app.get("column")) == 3 and all("**Verdict:" in a.value for a in app.text_area)
    checks["inherited_chart_and_provenance_visible"] = bool(app.get("vega_lite_chart")) and bool(app.json) and "not investment advice" in app.caption[0].value
    injection = []
    for index, investor in enumerate(("Buffett", "Graham", "Burry")):
        original = app.text_area[index].value
        app.text_area[index].set_value(original + "\nInjected ratio 987654321.12345.").run()
        detected = any(investor in e.value and "987654321.12345" in e.value for e in app.error)
        app.button[0].click().run()
        injection.append(detected and not app.error and app.text_area[index].value == original)
    checks["numeric_injection_flag_and_reload_work_for_every_memo"] = all(injection)
    app.sidebar.checkbox[0].check().run()
    checks["threshold_probe_in_real_app"] = list(app.table[0].value["Result"]) == ["pass"] * 8 and any("Temporary probe" in w.value for w in app.warning)
    app.sidebar.checkbox[0].uncheck().run()
    checks["baseline_restored_after_probe"] = app.table[0].value.iloc[3]["Result"] == "fail"
    app.sidebar.text_input[0].set_value("JPM").run()
    checks["JPM_gaps_and_all_three_memos_visible"] = (
        not app.exception and not app.error and len(app.text_area) == 3
        and set(app.dataframe[0].value["current_ratio"]) == {"not known"}
        and set(app.dataframe[0].value["capital_spending"]) == {"not found"}
        and list(app.table[0].value["Result"]) == ["fail", "not known", "not known", "not known", "pass", "pass", "fail", "fail"])
    app.sidebar.text_input[0].set_value("../../COST").run()
    checks["invalid_ticker_handled"] = not app.exception and bool(app.error) and not app.dataframe
    app.sidebar.text_input[0].set_value("ZZLAB").run()
    checks["unknown_ticker_handled"] = not app.exception and bool(app.error) and not app.dataframe
    result = {"method": "Streamlit AppTest on actual page; offline SEC snapshots; no browser screenshot", "checks": {k: bool(v) for k, v in checks.items()}}
    (HERE / "app-verification-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return all(checks.values())


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
