"""Reproduce course answers through the engine and actual Streamlit page."""
import copy
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest
import portfolio as p
from analyze_personal import calculate

ROOT = Path(__file__).resolve().parent


def signature(result):
    return ([round(x * 100) for x in result["weights"].values()],
            f"{result['return'] * 100:.2f}", f"{result['volatility'] * 100:.2f}")


class Lab15Audit(unittest.TestCase):
    def test_cli_unchanged(self):
        before = subprocess.check_output([sys.executable, str(ROOT.parent / "lab-14-portfolio-baselines/portfolio.py")])
        after = subprocess.check_output([sys.executable, str(ROOT / "portfolio.py")])
        self.assertEqual(before, after)

    def test_known_answers_and_constraints(self):
        loaded = p.search_mix(p.SLEEVES, p.CORRELATIONS)
        self.assertEqual(signature(loaded), ([0, 20, 25, 55], "6.51", "9.44"))
        changed = copy.deepcopy(p.SLEEVES)
        changed["Global equity index fund"]["return"] = .07
        attack = p.search_mix(changed, p.CORRELATIONS)
        self.assertEqual(signature(attack), ([0, 10, 10, 80], "6.53", "12.94"))
        self.assertAlmostEqual(max(abs(attack["weights"][k] - loaded["weights"][k]) for k in p.SLEEVES) * 100, 25)
        self.assertIsNone(p.search_mix(p.SLEEVES, p.CORRELATIONS, .09, .03))
        for inputs, result in [(p.SLEEVES, loaded), (changed, attack)]:
            self.assertAlmostEqual(sum(result["weights"].values()), 1)
            self.assertGreaterEqual(result["return"] + 1e-12, .065)
            self.assertGreaterEqual(result["reserve"] + 1e-12, .03)
            self.assertTrue(all(w >= 0 and math.isclose(w * 20, round(w * 20)) for w in result["weights"].values()))
        no_reserves = copy.deepcopy(p.SLEEVES)
        for inputs in no_reserves.values():
            inputs["reserve_eligible"] = False
        self.assertIsNone(p.search_mix(no_reserves, p.CORRELATIONS))
        self.assertIsNotNone(p.search_mix(no_reserves, p.CORRELATIONS, reserve_minimum=0))

    def test_actual_page_and_engine_source_change(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric][:3], ["6.51%", "9.44%", "20.00%"])
        next(n for n in app.number_input if n.label == "Global equity index fund expected return (%)").set_value(7.0).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["6.53%", "12.94%", "10.00%", "6.51%", "9.44%", "20.00%", "25.00"])
        # A separate process avoids imported module caches; modify BOTH actual
        # source cells in a temporary app package and test the rendered page.
        source = (ROOT / "portfolio.py").read_text(encoding="utf-8")
        altered = source.replace("0.80, 1.00, 0.25", "0.80, 1.00, 0.50").replace("-0.10, 0.25, 1.00", "-0.10, 0.50, 1.00")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "portfolio.py").write_text(altered, encoding="utf-8")
            (path / "app.py").write_text((ROOT / "app.py").read_text(encoding="utf-8"), encoding="utf-8")
            script = "from streamlit.testing.v1 import AppTest; a=AppTest.from_file('app.py').run(); assert not a.exception; assert [m.value for m in a.metric][:3]==['6.52%', '9.73%', '40.00%']; rows=a.table[0].value; assert rows['Weight (%)'].tolist()==['0.00','40.00','0.00','60.00']; print('Changed engine source reaches rendered app: PASS')"
            probe = subprocess.run([sys.executable, "-c", script], cwd=folder, capture_output=True, text=True)
            self.assertEqual(probe.returncode, 0, probe.stdout + probe.stderr)
        self.assertEqual(p.CORRELATIONS[2][3], .25)
        self.assertEqual(p.CORRELATIONS[3][2], .25)
        next(n for n in app.number_input if n.label == "Objective return (%)").set_value(20.0).run()
        self.assertEqual(len(app.warning), 2)
        self.assertTrue(all(w.value == "no mix meets the objective" for w in app.warning))

    def test_csv_estimates_and_rejections(self):
        # Synthetic prices ONLY for software testing, never submission evidence.
        dates = pd.date_range("2021-01-31", periods=61, freq="ME")
        frame = pd.DataFrame({"Date": dates})
        for i, name in enumerate(["TEST_A", "TEST_B", "TEST_C"]):
            returns = pd.Series([.003 + .004 * math.sin(t * (i + 1)) + .0001 * t for t in range(60)])
            frame[name] = [100] + (100 * (1 + returns).cumprod()).tolist()
        csv = lambda f: io.StringIO(f.to_csv(index=False))
        full, correlations, meta = p.estimate_from_csv(csv(frame))
        recent, _, recent_meta = p.estimate_from_csv(csv(frame), True)
        direct = frame.iloc[:, 1:].pct_change(fill_method=None).iloc[1:]
        self.assertEqual(meta["return_months"], 60)
        self.assertEqual(recent_meta["return_months"], 36)
        for name in full:
            self.assertAlmostEqual(full[name]["return"], direct[name].mean() * 12)
            self.assertAlmostEqual(full[name]["volatility"], direct[name].std(ddof=1) * math.sqrt(12))
            self.assertAlmostEqual(recent[name]["return"], direct[name].tail(36).mean() * 12)
        self.assertAlmostEqual(correlations[0][1], direct.corr().iloc[0, 1])
        invalids = [frame.iloc[::-1], frame.drop(index=3), frame.iloc[:30]]
        missing = frame.copy()
        missing.loc[2, "TEST_A"] = float("nan")
        invalids.append(missing)
        for invalid in invalids:
            with self.assertRaises(ValueError):
                p.estimate_from_csv(csv(invalid))
        with self.assertRaisesRegex(ValueError, "unique"):
            p.estimate_from_csv(io.StringIO("Date,TEST_A,TEST_A,TEST_C\n"))

    def test_personal_source_prices_and_results(self):
        results = calculate()  # Also checks exact file hashes and window counts.
        self.assertEqual(signature(results["runs"]["all_months"]), ([0, 70, 25, 5], "21.55", "24.82"))
        self.assertEqual(signature(results["runs"]["last_36"]), ([0, 55, 45, 0], "39.62", "21.69"))
        self.assertEqual(signature(results["runs"]["TSM_minus_1_point"]), ([0, 70, 25, 5], "21.30", "24.82"))
        self.assertAlmostEqual(results["largest_window_change_points"], 20)
        self.assertAlmostEqual(results["largest_attack_change_points"], 0)
        self.assertTrue(all(asset["return"] > .10 for asset in results["estimates_all"].values()))
        # Independently reconcile every monthly CSV price to the saved Yahoo
        # daily adjusted-close response, not to a second generated summary.
        csv = pd.read_csv(ROOT / "prices.csv", index_col="Date")
        for ticker in csv.columns:
            raw = json.loads((ROOT / "sources" / f"{ticker}-yahoo-daily.json").read_text(encoding="utf-8"))
            source = raw["chart"]["result"][0]
            dates = pd.to_datetime(source["timestamp"], unit="s", utc=True).tz_localize(None)
            values = source["indicators"]["adjclose"][0]["adjclose"]
            daily = pd.Series(values, index=dates)
            monthly = daily.groupby(daily.index.to_period("M")).last()
            for date, value in csv[ticker].items():
                period = pd.Timestamp(date).to_period("M")
                actual = monthly.loc[period]
                self.assertAlmostEqual(value, actual, places=10)

    def test_personal_saved_data_in_actual_page(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run()
        next(c for c in app.checkbox if c.label == "Use my saved Project 2 prices.csv").check().run()
        self.assertFalse(app.exception)
        self.assertEqual(next(n for n in app.number_input if n.label == "Objective return (%)").value, 10)
        self.assertEqual(next(n for n in app.number_input if n.label == "Reserve minimum (%)").value, 0)
        self.assertEqual([m.value for m in app.metric][:3], ["21.55%", "24.82%", "0.00%"])
        next(c for c in app.checkbox if c.label == "Use last 36 monthly returns").check().run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["39.62%", "21.69%", "0.00%", "21.55%", "24.82%", "0.00%", "20.00"])
        next(c for c in app.checkbox if c.label == "Use last 36 monthly returns").uncheck().run()
        tsm = next(n for n in app.number_input if n.label == "TSM expected return (%)")
        tsm.set_value(tsm.value - 1).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["21.30%", "24.82%", "0.00%", "21.55%", "24.82%", "0.00%", "0.00"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
