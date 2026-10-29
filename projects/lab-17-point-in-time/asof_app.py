"""Lab 17: public FRED values versus an actual ALFRED vintage, without a key."""

from datetime import date, datetime, timezone
from io import StringIO
import re

import pandas as pd
import requests
import streamlit as st

SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]+", series_id):
        raise ValueError("Use a FRED series ID containing letters, numbers, or underscores.")
    return series_id


def parse_csv(text, expected_column):
    """Require the series and an eligible vintage: ALFRED may label its last release."""
    frame = pd.read_csv(StringIO(text), na_values=["."], keep_default_na=True)
    actual_column = frame.columns[1] if len(frame.columns) == 2 else ""
    eligible = actual_column == expected_column
    expected_vintage = re.fullmatch(r"(.+)_(\d{8})", expected_column)
    if expected_vintage and not eligible:
        series_id, requested_day = expected_vintage.groups()
        actual_vintage = re.fullmatch(re.escape(series_id) + r"_(\d{8})", actual_column)
        if actual_vintage:
            actual_day = datetime.strptime(actual_vintage.group(1), "%Y%m%d").date()
            eligible = actual_day <= datetime.strptime(requested_day, "%Y%m%d").date()
    if len(frame.columns) != 2 or frame.columns[0] != "observation_date" or not eligible:
        raise ValueError(f"Unexpected CSV columns; expected observation_date,{expected_column}.")
    frame = frame.rename(columns={actual_column: expected_column})
    frame["observation_date"] = pd.to_datetime(frame["observation_date"], errors="raise")
    frame[expected_column] = pd.to_numeric(frame[expected_column], errors="raise")
    frame = frame.rename(columns={"observation_date": "date", expected_column: "value"})
    if frame["date"].isna().any() or frame["date"].duplicated().any():
        raise ValueError("Missing or duplicate observation dates.")
    values = frame["value"].dropna()
    if values.isin([float("inf"), float("-inf")]).any():
        raise ValueError("Nonfinite observations.")
    return frame.set_index("date").sort_index()


def download(url, expected_column):
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    return {"data": parse_csv(response.text, expected_column), "csv": response.text,
            "url": response.url,
            "downloaded_at_utc": datetime.now(timezone.utc).isoformat()}


@st.cache_data(ttl=3600, show_spinner=False)
def download_current(series_id, download_day):
    """One public CSV request per series/cache miss; day prevents overnight reuse."""
    series_id = validate_id(series_id)
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    return download(url, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_vintage(series_id, as_known_on, download_day):
    """Get what ALFRED actually archived on the chosen day; never fall back to FRED."""
    series_id = validate_id(series_id)
    cutoff = date.fromisoformat(as_known_on)
    if cutoff > date.today():
        raise ValueError("The as-known date cannot be in the future.")
    url = (f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
           f"&vintage_date={cutoff.isoformat()}")
    column = f"{series_id}_{cutoff:%Y%m%d}"
    result = download(url, column)
    if (result["data"].dropna().index > pd.Timestamp(cutoff)).any():
        raise ValueError("Vintage contains observations measured after the cutoff.")
    return result


def compare(current, vintage):
    """Count only nonmissing observations and compare matching measured dates."""
    now = current["value"].dropna()
    then = vintage["value"].dropna()
    latest_then = then.index.max() if not then.empty else None
    latest_now = now.index.max() if not now.empty else None
    common = now.index.intersection(then.index)
    revised = now.loc[common].sub(then.loc[common]).abs().gt(1e-9)
    return {
        "Last measured date known then": latest_then,
        "Value known then": float(then.iloc[-1]) if not then.empty else None,
        "Last measured date today": latest_now,
        "Value today": float(now.iloc[-1]) if not now.empty else None,
        "Later values today": int((now.index > latest_then).sum()) if latest_then is not None else len(now),
        "Revised matching dates": int(revised.sum()),
        "Matching dates compared": len(common),
    }


def main():
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    today = date.today()
    day = today.isoformat()
    st.title("Point-in-Time Rates Audit")
    st.caption(f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({day}); "
               "built with AI help, a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES),
                                     format_func=lambda s: f"{s} — {SERIES[s]}")
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="For example, PAYEMS")
    start = st.sidebar.date_input("Chart start date", date(2020, 1, 1),
                                 min_value=date(1776, 1, 1), max_value=today)
    cutoff = st.sidebar.date_input("As known on", today,
                                  min_value=date(1776, 1, 1), max_value=today)
    if st.sidebar.button("Refresh downloads"):
        download_current.clear()
        download_vintage.clear()
    if extra.strip():
        try:
            added = validate_id(extra)
            if added not in selected:
                selected.append(added)
        except ValueError as error:
            st.error(str(error))
    st.info("Charts show today's vintage. The table compares the entire downloaded history; "
            "the chart start date does not change the counts. Monthly dates label the month measured, "
            "not the release day. ALFRED's date is a daily vintage, not proof of intraday availability.")
    rows = []
    for series_id in selected:
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Additional FRED series')}")
        try:
            with st.spinner(f"Downloading {series_id}…"):
                current = download_current(series_id, day)
                vintage = download_vintage(series_id, cutoff.isoformat(), day)
            row = compare(current["data"], vintage["data"])
            chart = current["data"].loc[pd.Timestamp(start):].rename(columns={"value": series_id})
            if chart.dropna().empty:
                st.warning("No current observations in the selected chart window.")
            else:
                st.line_chart(chart)
            last = row["Last measured date known then"]
            label = last.strftime("%Y-%m-%d") if last is not None else "none (no published values)"
            st.write(f"Last measured date known on {cutoff}: **{label}**")
            st.caption(f"[FRED series](https://fred.stlouisfed.org/series/{series_id}) · "
                       f"[Current CSV]({current['url']}) · [Vintage CSV]({vintage['url']}) · "
                       f"Downloaded UTC: current {current['downloaded_at_utc']}; vintage {vintage['downloaded_at_utc']}")
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{series_id}", **row})
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            st.error(f"{series_id}: {error}")
    st.subheader("As-known comparison")
    st.caption("Later values = today's nonmissing values after the last measured date known then "
               "(all current values if no vintage values exist). Revised = changed nonmissing "
               "values on dates present in both downloads, tolerance 1e-9; missing days are never filled.")
    if rows:
        table = pd.DataFrame(rows)
        st.dataframe(table, hide_index=True, column_config={
            "Series": st.column_config.LinkColumn("Series", display_text=r"series/(.*)"),
            "Last measured date known then": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "Last measured date today": st.column_config.DateColumn(format="YYYY-MM-DD"),
        })
        st.download_button("Download comparison CSV", table.to_csv(index=False),
                           file_name=f"asof-comparison-{cutoff}.csv", mime="text/csv")
    elif not selected:
        st.info("Select a series or add a FRED ID to begin.")


if __name__ == "__main__":
    main()
