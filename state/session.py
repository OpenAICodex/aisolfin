"""Session state helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import streamlit as st


@dataclass(frozen=True)
class SessionKeys:
    current_page: str = "current_page"
    selected_process: str = "selected_process"
    modal_open: str = "modal_open"
    toast_message: str = "toast_message"


KEYS = SessionKeys()


def bootstrap(default_page: str = "Dashboard") -> None:
    """Initialize canonical session state entries."""

    if KEYS.current_page not in st.session_state:
        st.session_state[KEYS.current_page] = default_page
    st.query_params["page"] = st.session_state[KEYS.current_page]


def sync_from_query() -> None:
    """Apply query parameters to session state."""

    page = st.query_params.get("page")
    if page:
        st.session_state[KEYS.current_page] = page


def update_query(**params: Any) -> None:
    """Update the URL query parameters in-place."""

    current = dict(st.query_params)
    current.update({k: v for k, v in params.items() if v is not None})
    st.query_params.update(current)
