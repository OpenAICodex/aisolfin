"""Utilities for injecting shared styles."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from tokens import css_variables, flatten_tokens


def inject_css() -> None:
    template = Path("styles/styles.css").read_text()
    css = template.format(**flatten_tokens(), css_variables=css_variables())
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
