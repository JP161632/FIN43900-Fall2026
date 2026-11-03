"""Streamlit view of the reusable Buffett EDGAR skill's computed output."""
import importlib.util
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / ".agents/skills/buffett-edgar/scripts/edgar_facts.py"
spec = importlib.util.spec_from_file_location("edgar_facts", SCRIPT)
edgar = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = edgar
spec.loader.exec_module(edgar)

st.set_page_config(page_title="Buffett business lens", layout="wide")
st.title("Buffett business lens")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker_input = st.sidebar.text_input("Ticker", "COST")
mode = st.sidebar.radio("SEC data", ["Saved SEC responses", "Download / refresh SEC responses"])
st.sidebar.caption("Live downloads require SEC_USER_AGENT in the launch environment: your name and email. No API key.")

try:
    ticker = edgar.ticker_symbol(ticker_input)
    # Live mode downloads only when requested; ordinary memo edits use the saved response.
    live = st.sidebar.button("Download now", disabled=mode == "Saved SEC responses")
    result = edgar.run(ticker, refresh=live, offline=not live)
except Exception as error:
    st.error(f"{type(error).__name__}: {error}")
    st.info("Run the skill script for this ticker first, or select live downloads and click Download now.")
    st.stop()

report = edgar.report_text(result)
st.subheader(f'{ticker} · {result["company"]}')
st.caption(f'SEC response retrieved {result["source"]["retrieved_utc"]}. Saved responses are a dated snapshot, not a fresh retrieval.')
st.markdown(f'[SEC company facts]({result["source"]["url"]})')

chart = pd.DataFrame({
    "Fiscal-year end": [row["fiscal_year_end"] for row in result["rows"]],
    "Owner earnings": [None if row["owner_earnings"]["value"] is None else row["owner_earnings"]["value"] / 1e6 for row in result["rows"]],
    "Net income": [None if row["net_income"]["value"] is None else row["net_income"]["value"] / 1e6 for row in result["rows"]],
}).set_index("Fiscal-year end")
st.line_chart(chart, y_label="USD millions")
if chart["Owner earnings"].isna().any():
    st.warning("Owner earnings: not found for missing periods. Missing values are not plotted as zero.")

fields = list(edgar.TAGS) + ["roe", "owner_earnings"]
table = pd.DataFrame([{"Fiscal-year end": row["fiscal_year_end"], **{
    field: edgar.display(row[field], field == "roe") for field in fields}}
    for row in result["rows"]])
st.caption("Amounts in USD millions; ROE uses year-end equity. Fiscal periods may contain different numbers of weeks.")
st.dataframe(table, hide_index=True, width="stretch")
st.table(pd.DataFrame(result["checks"].items(), columns=["Buffett check", "Result"]))
with st.expander("XBRL tags and filing provenance"):
    st.dataframe(pd.DataFrame([{
        "Fiscal-year end": row["fiscal_year_end"], "Metric": field,
        "Tag / formula": row[field]["tag"], "Filed": row[field].get("filed", "derived"),
        "Accession": row[field].get("accession", ""),
    } for row in result["rows"] for field in fields]), hide_index=True)
    st.json(result)
st.download_button("Download computed report", report, file_name=f"{ticker}-report.md")

st.subheader("Buffett-style memo · AI simulation")
memo_path = HERE / "memos" / f"{ticker}.md"
saved = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
memo_key = f"memo_{ticker}"
if memo_key not in st.session_state:
    st.session_state[memo_key] = saved
if st.button("Reload memo from file"):
    st.session_state[memo_key] = saved
if not saved:
    st.info(f"No saved memo for {ticker}. Ask Codex to use $buffett-edgar on {ticker}; the model writes the judgment after running the script.")
memo = st.text_area("Memo (edit here to probe an unsupported number)", height=300, key=memo_key)
flags = edgar.unsupported_numbers(memo, report)
if flags:
    st.error("Unsupported memo numbers: " + ", ".join(item["token"] for item in flags))
    st.table(pd.DataFrame(flags))
elif memo.strip():
    st.success("Every numeric token occurs in the script's printed output.")
st.caption("This check preserves percent units and sign. It cannot prove a supported number was attached to the correct metric or that a qualitative claim is true.")
st.markdown(memo or "Memo pending.")
if st.button("Save memo edits"):
    memo_path.parent.mkdir(parents=True, exist_ok=True)
    memo_path.write_text(memo, encoding="utf-8")
    st.success(f"Saved memos/{ticker}.md. Unsupported-number flags remain visible above.")
st.download_button("Download memo", memo, file_name=f"{ticker}.md")
