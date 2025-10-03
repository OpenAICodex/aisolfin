"""Empty state component."""
from __future__ import annotations

import streamlit as st


def empty_state(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class='base-empty'>
          <div class='heading-3'>{title}</div>
          <div class='body-text'>{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
