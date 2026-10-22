"""Run: python -m streamlit run app.py"""
import copy
import hashlib
import importlib
import io
from pathlib import Path

import streamlit as st
import portfolio

# Reload the source on each page rerun so an engine-input edit reaches the app.
engine = importlib.reload(portfolio)
st.set_page_config(page_title="Lab 15 | Portfolio stability", layout="wide")
st.title("Lowest-risk mix under your mandate")
st.caption("Built with AI help, a learning demonstration, not investment advice.")
st.write("Search every long-only, fully invested mix in 5 percentage-point steps.")

saved_prices = Path(__file__).resolve().parent / "prices.csv"
use_saved = st.sidebar.checkbox("Use my saved Project 2 prices.csv", value=False, disabled=not saved_prices.exists())
mode = "personal" if use_saved else "training"
objective = st.sidebar.number_input("Objective return (%)", value=10.0 if use_saved else 6.5, step=0.1, key=f"objective:{mode}")
reserve_min = st.sidebar.number_input("Reserve minimum (%)", min_value=0.0, max_value=100.0, value=0.0 if use_saved else 3.0, step=1.0, key=f"reserve_min:{mode}")
uploaded = st.sidebar.file_uploader("Monthly adjusted prices CSV", type=["csv"])
last_36 = st.sidebar.checkbox("Use last 36 monthly returns", value=False)
if st.sidebar.button("Reload engine inputs"):
    st.rerun()

try:
    if uploaded is None and not use_saved:
        loaded = copy.deepcopy(engine.SLEEVES)
        current = copy.deepcopy(loaded)
        loaded_corr = current_corr = engine.CORRELATIONS
        source_key = "meridian"
        st.info("Meridian: course-authored training inputs, not market estimates.")
        if last_36:
            st.caption("The window switch applies after you upload monthly prices.")
    else:
        data = uploaded.getvalue() if uploaded is not None else saved_prices.read_bytes()
        if uploaded is not None and use_saved:
            st.caption("Uploaded prices take precedence over the saved Project 2 CSV.")
        source_key = hashlib.sha256(data).hexdigest()[:12] + str(last_36)
        loaded, loaded_corr, full_meta = engine.estimate_from_csv(io.BytesIO(data))
        current, current_corr, meta = engine.estimate_from_csv(io.BytesIO(data), last_36)
        st.info("Historical arithmetic return estimates, not forecasts. Monthly mean × 12; sample standard deviation × √12; monthly correlations. No costs deducted.")
        st.caption(f"Prices: {full_meta['price_start']} to {full_meta['price_end']} ({full_meta['price_rows']} rows). Current estimate: {meta['return_months']} monthly returns, {meta['return_start']} to {meta['return_end']}.")
        if full_meta["price_rows"] < 60:
            st.warning("The lab requires five years of monthly prices; this upload has fewer than 60 rows.")

    st.subheader("Edit expected return estimates and reserve eligibility")
    for name, inputs in current.items():
        left, right = st.columns(2)
        inputs["return"] = left.number_input(f"{name} expected return (%)", value=float(inputs["return"] * 100), step=1.0, key=f"return:{source_key}:{name}") / 100
        eligible = right.checkbox(f"{name}: reserve eligible", value=bool(inputs["reserve_eligible"]), key=f"reserve:{source_key}:{name}")
        inputs["reserve_eligible"] = loaded[name]["reserve_eligible"] = eligible

    answer = engine.search_mix(current, current_corr, objective / 100, reserve_min / 100)
    baseline = engine.search_mix(loaded, loaded_corr, objective / 100, reserve_min / 100)
    st.caption("Both answers use the current objective and reserve rule. The loaded comparison keeps original return estimates and, for CSVs, all months.")

    def show_result(column, title, result):
        with column:
            st.subheader(title)
            if result is None:
                st.warning("no mix meets the objective")
                return
            st.table([{"Asset": name, "Weight (%)": f"{weight * 100:.2f}"} for name, weight in result["weights"].items()])
            st.metric("Expected return", f"{result['return']:.2%}")
            st.metric("Volatility", f"{result['volatility']:.2%}")
            st.metric("Reserve-eligible weight", f"{result['reserve']:.2%}")

    left, right = st.columns(2)
    show_result(left, "Current inputs", answer)
    show_result(right, "Inputs as loaded (all months)", baseline)
    if answer is not None and baseline is not None:
        change = max(abs(answer["weights"][name] - baseline["weights"][name]) for name in loaded) * 100
        st.metric("Largest weight change (percentage points)", f"{change:.2f}")
    else:
        st.write("Largest weight change: unavailable because at least one run has no feasible mix.")
    st.caption("Minimum estimated volatility on this grid under the return and reserve rules. Other mandate restrictions require separate checks. A 3% reserve floor requires at least 5% eligible weight on this grid.")
except (ValueError, KeyError, TypeError) as error:
    st.error(str(error))
