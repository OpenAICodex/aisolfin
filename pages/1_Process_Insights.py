"""Process insights detail view."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from components import badge, card, data_table, toolbar
from services.api import ApiClient, fetch_processes
from state import session
from styles import inject_css


def main() -> None:
    st.set_page_config(page_title="Process Insights", page_icon="📊", layout="wide")
    session.bootstrap("Processes")
    session.sync_from_query()
    inject_css()

    client = ApiClient()
    processes = fetch_processes(client)
    toolbar("Process insights", "Compare optimization streams across owners.")

    df = pd.DataFrame(
        [
            {
                "ID": process.id,
                "Name": process.name,
                "Owner": process.owner,
                "Status": process.status,
                "Throughput": process.throughput,
                "Efficiency": process.efficiency * 100,
            }
            for process in processes
        ]
    )

    with card(title="Process catalogue", flush=True):
        data_table(df, key="insights-table", page_size=10)

    with card(title="Status breakdown"):
        counts = df.groupby("Status").size().reset_index(name="count")
        for _, row in counts.iterrows():
            badge(f"{row['Status']} — {row['count']} streams", variant="info")


if __name__ == "__main__":
    main()
