"""Toast notifications."""
from __future__ import annotations

from typing import Literal

import streamlit as st

Variant = Literal["default", "success", "danger", "info"]


def toast(message: str, variant: Variant = "default", key: str = "toast") -> None:
    """Render a toast message."""

    classes = ["base-toast"]
    if variant != "default":
        classes.append(f"base-toast--{variant}")
    placeholder = st.empty()
    placeholder.markdown(
        f"<div class='{' '.join(classes)}' id='{key}'>{message}</div>",
        unsafe_allow_html=True,
    )
