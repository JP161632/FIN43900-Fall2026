"""Independent known-answer and failure-injection audit. Standard library only."""

import contextlib
import copy
import importlib.util
import io
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import portfolio as p

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent


def load_mandate():
    path = ROOT.parent / "lab-13-portfolio-mandate" / "mandate.py"
    spec = importlib.util.spec_from_file_location("lab13_mandate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortfolioAudit(unittest.TestCase):
    def test_all_published_baseline_values(self):
        known = {
            "Benchmark": (["0.0", "0.0", "40.0", "60.0"], "6.80", "10.46", "0.0", True),
            "Equal weight": (["25.0"] * 4, "5.20", "5.21", "50.0", False),
            "Inverse volatility": (["84.3", "6.0", "7.0", "2.6"], "3.77", "1.05", "90.3", False),
        }
        covariance = p.covariance_matrix(p.SLEEVES, p.CORRELATIONS)
        for name, weights in p.baseline_portfolios(p.SLEEVES).items():
            with self.subTest(portfolio=name):
                expected_weights, ret, vol, reserve, meets = known[name]
                self.assertEqual([f"{weights[key] * 100:.1f}" for key in p.SLEEVES], expected_weights)
                self.assertEqual(f"{p.expected_return(weights, p.SLEEVES) * 100:.2f}", ret)
                self.assertEqual(f"{p.portfolio_volatility(weights, p.SLEEVES, covariance) * 100:.2f}", vol)
                self.assertEqual(f"{p.reserve_eligible_weight(weights, p.SLEEVES) * 100:.1f}", reserve)
                self.assertEqual(p.meets_objective(p.expected_return(weights, p.SLEEVES), p.OBJECTIVE_RETURN), meets)
                self.assertAlmostEqual(sum(weights.values()), 1)
                self.assertTrue(all(0 <= value <= 1 for value in weights.values()))

    def test_independent_two_asset_formula(self):
        # Handout digits in percentage units; independent of the matrix functions.
        by_hand = math.sqrt(0.4**2 * 6**2 + 0.6**2 * 16**2 + 2 * 0.4 * 0.6 * 0.25 * 6 * 16)
        actual = p.portfolio_volatility(p.BENCHMARK_WEIGHTS, p.SLEEVES, p.covariance_matrix(p.SLEEVES, p.CORRELATIONS)) * 100
        self.assertAlmostEqual(actual, by_hand)
        self.assertAlmostEqual(by_hand, 10.461357464497617)

    def test_changed_correlation_and_restoration(self):
        changed = copy.deepcopy(p.CORRELATIONS)
        changed[2][3] = changed[3][2] = 0.50
        risk = p.portfolio_volatility(p.BENCHMARK_WEIGHTS, p.SLEEVES, p.covariance_matrix(p.SLEEVES, changed))
        self.assertEqual(f"{risk * 100:.2f}", "11.00")
        self.assertEqual(p.CORRELATIONS[2][3], 0.25)
        self.assertEqual(p.CORRELATIONS[3][2], 0.25)
        source = (ROOT / "portfolio.py").read_text(encoding="utf-8")
        content = source.replace("0.80, 1.00, 0.25", "0.80, 1.00, 0.50").replace("-0.10, 0.25, 1.00", "-0.10, 0.50, 1.00")
        with tempfile.TemporaryDirectory() as folder:
            probe = Path(folder) / "portfolio.py"
            probe.write_text(content, encoding="utf-8")
            run = subprocess.run([sys.executable, str(probe)], capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            benchmark = run.stdout.split("\nBenchmark\n")[1].split("\nEqual weight\n")[0]
            self.assertIn("Volatility: 11.00%", benchmark)

    def test_actual_cli_refuses_bad_and_asymmetric_inputs(self):
        source = (ROOT / "portfolio.py").read_text(encoding="utf-8")
        probes = [
            (source.replace("0.80, 1.00, 0.25", "0.80, 1.00, 1.3").replace("-0.10, 0.25, 1.00", "-0.10, 1.3, 1.00"), "between -1 and 1"),
            (source.replace("0.80, 1.00, 0.25", "0.80, 1.00, 0.50"), "symmetric"),
        ]
        with tempfile.TemporaryDirectory() as folder:
            probe = Path(folder) / "portfolio.py"
            for content, message in probes:
                with self.subTest(message=message):
                    self.assertNotEqual(content, source)
                    probe.write_text(content, encoding="utf-8")
                    run = subprocess.run([sys.executable, str(probe)], capture_output=True, text=True, check=False)
                    self.assertEqual(run.returncode, 1)
                    self.assertIn(message, run.stderr)
                    self.assertNotIn("Expected return:", run.stdout)

    def test_covariance_order_symmetry_and_diagonal(self):
        covariance = p.covariance_matrix(p.SLEEVES, p.CORRELATIONS)
        self.assertAlmostEqual(covariance[2][3], 0.0024)
        for i, inputs in enumerate(p.SLEEVES.values()):
            self.assertAlmostEqual(covariance[i][i], inputs["volatility"] ** 2)
            for j in range(len(p.SLEEVES)):
                self.assertAlmostEqual(covariance[i][j], covariance[j][i])
        # Dict insertion order of the weights must not change the answer.
        reversed_weights = dict(reversed(list(p.BENCHMARK_WEIGHTS.items())))
        self.assertAlmostEqual(p.portfolio_volatility(reversed_weights, p.SLEEVES, covariance), p.portfolio_volatility(p.BENCHMARK_WEIGHTS, p.SLEEVES, covariance))

    def test_invalid_matrices_and_rates(self):
        for value in (-1.3, float("nan"), float("inf")):
            changed = copy.deepcopy(p.CORRELATIONS)
            changed[2][3] = changed[3][2] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                p.covariance_matrix(p.SLEEVES, changed)
        with self.assertRaises(ValueError):
            p.covariance_matrix(p.SLEEVES, [[1]])
        changed = copy.deepcopy(p.SLEEVES)
        changed["Treasury bills"]["volatility"] = 0
        with self.assertRaises(ValueError):
            p.covariance_matrix(changed, p.CORRELATIONS)
        invalid = [[1, .9, .9, 0], [.9, 1, -.9, 0], [.9, -.9, 1, 0], [0, 0, 0, 1]]
        with self.assertRaisesRegex(ValueError, "positive semidefinite"):
            p.covariance_matrix(p.SLEEVES, invalid)

    def test_benchmark_candidate_e_fails_reserve_only(self):
        mandate = load_mandate()
        expected = {name: p.BENCHMARK_WEIGHTS.get(name, 0) * 100 for name in mandate.HOLDINGS}
        self.assertEqual(mandate.CANDIDATES["E"], expected)
        minimum = mandate.QUARTERS_TO_COVER * mandate.QUARTERLY_DISTRIBUTION / mandate.RESERVE_SIZE * 100
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            mandate.check_candidate("E", expected, minimum)
        text = output.getvalue()
        self.assertIn("Reserve >= 3.0%: 0.0 FAIL", text)
        self.assertIn("Verdict: fails 1 rule(s)", text)

    def test_invalid_weight_labels_and_objective_boundary(self):
        with self.assertRaisesRegex(ValueError, "labels"):
            p.expected_return({"wrong label": 1}, p.SLEEVES)
        changed = dict(p.BENCHMARK_WEIGHTS)
        changed["Treasury bills"] = -0.1
        with self.assertRaises(ValueError):
            p.expected_return(changed, p.SLEEVES)
        self.assertTrue(p.meets_objective(0.065, 0.065))
        self.assertFalse(p.meets_objective(0.064999, 0.065))

if __name__ == "__main__":
    unittest.main(verbosity=2)
