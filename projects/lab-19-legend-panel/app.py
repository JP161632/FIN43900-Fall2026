"""Lab 19 companion to the preserved Lab 18 Streamlit app."""
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import panel

st.set_page_config(page_title="Legend panel", layout="wide")
st.title("Legend panel: Buffett · Graham · Burry")
st.caption("Data from SEC EDGAR; a learning demonstration, not investment advice.")
ticker_input = st.sidebar.text_input("Ticker", "COST")
mode = st.sidebar.radio("SEC data", ["Saved SEC responses", "Download / refresh SEC responses"])
st.sidebar.caption("Live downloads require SEC_USER_AGENT in the launch environment. No API key; identity is never saved.")
probe = st.sidebar.checkbox("Probe Graham threshold at 1.0", value=False)
try:
    ticker = panel.edgar.ticker_symbol(ticker_input)
    live = st.sidebar.button("Download now", disabled=mode == "Saved SEC responses")
    result = panel.run(ticker, refresh=live, offline=not live, hurdle=1.0 if probe else None)
except Exception as error:
    st.error(f"{type(error).__name__}: {error}")
    st.info("Run panel.py for this ticker first, or select live downloads and click Download now.")
    st.stop()

report = panel.report_text(result)
st.subheader(f'{ticker} · {result["company"]}')
st.caption(f'Original SEC retrieval: {result["source"]["retrieved_utc"]}. Saved responses are a dated snapshot.')
st.markdown(f'[SEC company facts]({result["source"]["url"]})')
if probe:
    st.warning("Temporary probe: Graham threshold is 1.0. Saved memos describe the retained setting and are not rewritten by this probe.")

chart = pd.DataFrame({"Fiscal-year end": [r["fiscal_year_end"] for r in result["rows"]], **{
    f: [None if r[f]["value"] is None else r[f]["value"] / 1e6 for r in result["rows"]]
    for f in ("owner_earnings", "net_income")}}).set_index("Fiscal-year end")
st.line_chart(chart, y_label="USD millions")
if chart["owner_earnings"].isna().any():
    st.warning("Owner earnings: not found for missing periods; gaps are not plotted as zero.")
fields = list(panel.edgar.TAGS) + ["roe", "owner_earnings"] + list(panel.EXTRA) + ["current_ratio", "liabilities_to_equity"]
st.caption("Amounts: USD millions. ROE: percent using year-end equity. Other ratios: times; checks use unrounded values.")
st.dataframe(pd.DataFrame([{"Fiscal-year end": r["fiscal_year_end"], **{
    f: panel.shown(r[f], f) for f in fields}} for r in result["rows"]]), hide_index=True, width="stretch")
st.subheader("Panel checks")
st.table(pd.DataFrame([{"Investor": i, "Check": name, "Result": outcome}
    for i, checks in result["panel"].items() for name, outcome in checks.items()]))
with st.expander("XBRL tags and selected filing provenance"):
    st.dataframe(pd.DataFrame([{"Fiscal-year end": r["fiscal_year_end"], "Metric": f,
        "Tag / formula": r[f]["tag"], "Filed": r[f].get("filed", "derived"),
        "Accession": r[f].get("accession", "")} for r in result["rows"] for f in fields]), hide_index=True)
    st.json(result)
st.download_button("Download computed report", report, file_name=f"{ticker}-panel-report.md")

st.subheader("Investor verdicts and memos · educational simulations")
saved = panel.load_memos(ticker)
for i in panel.INVESTORS:
    key = f"memo_{ticker}_{i}"
    if key not in st.session_state:
        st.session_state[key] = saved[i]
if st.button("Reload all memos from files"):
    for i in panel.INVESTORS:
        st.session_state[f"memo_{ticker}_{i}"] = saved[i]
edited = {}
for column, investor in zip(st.columns(3), panel.INVESTORS):
    with column:
        st.markdown(f"### {investor}")
        st.caption(panel.summary(result["panel"][investor]))
        edited[investor] = st.text_area(f"{investor} memo", key=f"memo_{ticker}_{investor}", height=360)
        st.markdown(f'**Investor verdict:** {panel.verdict(edited[investor])}')
        st.markdown(edited[investor] or "Memo pending. Run the corresponding skill after printing this ticker's facts.")
        if st.button(f"Save {investor} memo"):
            path = panel.memo_path(ticker, investor)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(edited[investor], encoding="utf-8")
            st.success("Memo saved; the numeric check remains visible below.")
        st.download_button(f"Download {investor} memo", edited[investor], file_name=f"{ticker}-{investor.lower()}.md")

st.subheader("Unprinted-number flag across all memos")
flags = panel.memo_flags(edited, report)
flag_rows = [{"Investor": i, **flag} for i, items in flags.items() for flag in items]
if flag_rows:
    st.error("Unsupported memo numbers: " + "; ".join(f'{r["Investor"]}: {r["token"]}' for r in flag_rows))
    st.table(pd.DataFrame(flag_rows))
elif any(not text.strip() for text in edited.values()):
    st.warning("Some memos are missing. An empty memo is not a validated judgment.")
else:
    st.success("All three memos: every numeric token occurs in the script's printed output.")
st.caption("Occurrence checking cannot establish correct metric attribution, truthful qualitative claims or independent corroboration.")
