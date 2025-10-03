"""Button component wrapper."""
from __future__ import annotations

from typing import Literal, Optional

import streamlit as st


ButtonKind = Literal["primary", "secondary", "ghost"]


def button(
    label: str,
    key: str,
    kind: ButtonKind = "primary",
    icon: Optional[str] = None,
    disabled: bool = False,
    help: Optional[str] = None,
) -> bool:
    """Render a themed button and return its click state."""

    if kind not in {"primary", "secondary", "ghost"}:
        raise ValueError(f"Unknown button kind: {kind}")

    wrapper = st.container()
    wrapper.markdown(
        f"<div class='base-button-wrapper base-button--{kind}'>",
        unsafe_allow_html=True,
    )

    display_label = f"{icon} {label}" if icon else label
    clicked = wrapper.button(display_label, key=key, disabled=disabled, help=help)

    wrapper.markdown("</div>", unsafe_allow_html=True)
    return clicked
