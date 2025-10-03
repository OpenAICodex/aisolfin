"""Badge component."""
from __future__ import annotations

from typing import Literal

import streamlit as st

Variant = Literal["default", "success", "danger", "info"]


def badge(label: str, variant: Variant = "default") -> None:
    """Render a badge inline."""

    variant_class = "base-badge" if variant == "default" else f"base-badge base-badge--{variant}"
    st.markdown(f"<span class='{variant_class}'>{label}</span>", unsafe_allow_html=True)
