"""
# Base44 Process Optimizer (Streamlit)

## Setup
1. Create a virtual environment for Python 3.11+.
2. Install dependencies with `pip install -r requirements.txt`.
3. Launch the experience using `streamlit run app.py`.

## Theming
- Update `tokens.py` to adjust the design system.
- Run the app; styles automatically sync from tokens into `styles/styles.css`.

## Override Tokens
- Modify any token values in `tokens.py`.
- Optional: extend `styles/styles.css` for layout-specific rules using the
  provided CSS variables.
"""
from __future__ import annotations

from typing import Callable

import pandas as pd
import plotly.express as px
import streamlit as st

from components import badge, button, card, data_table, empty_state, input_field, modal, select_field, toolbar
from services import auth
from services.api import ApiClient, fetch_history, fetch_metrics, fetch_processes
from state import session
from styles import inject_css


def _set_page_config() -> None:
    st.set_page_config(
        page_title="Base44 Process Optimizer",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def _render_sidebar(navigate: Callable[[str], None]) -> None:
    user = auth.current_user()
    st.sidebar.image("https://placehold.co/160x40?text=Base44", use_column_width=True)
    st.sidebar.markdown("---")
    if user:
        st.sidebar.markdown(f"**{user.name}**\n\n{user.email}")
        if st.sidebar.button("Sign out", key="sidebar-signout"):
            auth.logout()
            st.experimental_rerun()
    else:
        st.sidebar.info("Sign in to access dashboards and controls.")

    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Go to",
        options=["Dashboard", "Processes"],
        index=["Dashboard", "Processes"].index(st.session_state[session.KEYS.current_page]),
    )
    navigate(page)


def _ensure_auth() -> bool:
    user = auth.current_user()
    if user:
        return True

    toolbar(
        title="Welcome to Base44",
        description="Authenticate to continue to the operations workspace.",
    )
    with card(title="Sign in"):
        with st.form("login-form"):
            email = input_field("login_email", "Work email", placeholder="alex@base44.com")
            password = input_field("login_password", "Password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in")
            if submitted:
                try:
                    auth.login(email, password)
                    st.experimental_rerun()
                except ValueError as exc:
                    st.error(str(exc))
    return False


def _render_metrics(metrics_df: pd.DataFrame) -> None:
    columns = st.columns(len(metrics_df))
    for col, (_, row) in zip(columns, metrics_df.iterrows()):
        with col:
            with card(flush=True):
                st.markdown(f"<div class='heading-3'>{row['label']}</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='heading-2'>{row['display_value']}</div>",
                    unsafe_allow_html=True,
                )
                trend_variant = "success" if row["trend"] >= 0 else "danger"
                trend_label = f"{'▲' if row['trend'] >= 0 else '▼'} {abs(row['trend']):.1f}%"
                badge(trend_label, variant=trend_variant)


def _render_history_chart(history: pd.DataFrame) -> None:
    with card(title="Throughput trend", flush=True):
        fig = px.area(
            history,
            x="timestamp",
            y="throughput",
            title="",
            color_discrete_sequence=["#3B5BCC"],
        )
        fig.update_traces(mode="lines+markers", hovertemplate="%{y} units")
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode="x unified",
            xaxis_title=None,
            yaxis_title="Units",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_process_table(processes_df: pd.DataFrame) -> None:
    with card(title="Active processes", subtitle="Performance snapshot", flush=True):
        response = data_table(processes_df, key="process-table", page_size=8)
        selected = response.get("selected_rows", []) if response else []
        if selected:
            st.session_state[session.KEYS.selected_process] = selected[0]["id"]
            st.session_state[session.KEYS.modal_open] = True

    selected_id = st.session_state.get(session.KEYS.selected_process)
    if selected_id and st.session_state.get(session.KEYS.modal_open):
        row = processes_df.loc[processes_df["id"] == selected_id].iloc[0]
        with modal(True, title=f"Process {row['id']}") as body:
            if body is not None:
                st.markdown(f"**Owner:** {row['owner']}")
                st.markdown(f"**Status:** {row['status']}")
                st.markdown(f"**Throughput:** {row['throughput']} units")
                st.markdown(f"**Efficiency:** {row['efficiency']}%")
                if button("Close", key="close-modal", kind="secondary"):
                    st.session_state[session.KEYS.modal_open] = False


def _render_process_form(client: ApiClient) -> None:
    with card(title="Add optimization stream"):
        with st.form("create-process"):
            name = input_field("new_process_name", "Process name")
            owner = select_field("new_process_owner", "Owner", options=["Amelia", "Noah", "Evelyn", "Kai"])
            status = select_field("new_process_status", "Status", options=["Active", "Monitoring", "Paused"])
            submitted = st.form_submit_button("Create process")
            if submitted:
                st.session_state[session.KEYS.toast_message] = f"Process '{name}' created for {owner}."
                st.success("Process created (mock)")

    toast_message = st.session_state.pop(session.KEYS.toast_message, None)
    if toast_message:
        from components import toast

        toast(toast_message, variant="info")


def _render_dashboard(client: ApiClient) -> None:
    metrics = fetch_metrics(client)
    history = fetch_history(client)
    processes = fetch_processes(client)

    metrics_df = pd.DataFrame(
        {
            "label": [m.label for m in metrics],
            "value": [m.value for m in metrics],
            "unit": [m.unit for m in metrics],
            "trend": [m.trend for m in metrics],
        }
    )
    metrics_df["display_value"] = metrics_df.apply(
        lambda row: f"{row['value']:.0f} {row['unit']}" if row["unit"] not in {"ratio", "%"} else f"{row['value']:.0%}",
        axis=1,
    )

    processes_df = pd.DataFrame(
        [
            {
                "id": process.id,
                "name": process.name,
                "owner": process.owner,
                "status": process.status,
                "throughput": process.throughput,
                "efficiency": process.efficiency * 100,
                "updated_at": process.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
            for process in processes
        ]
    )

    def _new_process_action() -> None:
        if button("New process", key="toolbar-new", kind="primary"):
            st.session_state[session.KEYS.toast_message] = "Use the Processes page to add new streams."

    toolbar(
        title="Operations overview",
        description="Monitor optimization streams, track throughput, and manage workloads.",
        actions=[_new_process_action],
    )

    _render_metrics(metrics_df)
    _render_history_chart(history)
    _render_process_table(processes_df)


def _render_processes(client: ApiClient) -> None:
    processes = fetch_processes(client)
    if not processes:
        empty_state("No processes", "Create a new optimization stream to get started.")
        return
    _render_process_form(client)


PAGES = {
    "Dashboard": _render_dashboard,
    "Processes": _render_processes,
}


def main() -> None:
    _set_page_config()
    session.bootstrap()
    session.sync_from_query()
    inject_css()

    client = ApiClient()

    def navigate(page: str) -> None:
        st.session_state[session.KEYS.current_page] = page
        session.update_query(page=page)

    _render_sidebar(navigate)

    if not _ensure_auth():
        return

    page = st.session_state[session.KEYS.current_page]
    render = PAGES.get(page, _render_dashboard)
    render(client)


if __name__ == "__main__":
    main()
