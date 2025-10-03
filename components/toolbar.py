"""Toolbar layout component."""
from __future__ import annotations

from typing import Callable, Iterable

import streamlit as st


def toolbar(
    title: str,
    description: str | None = None,
    actions: Iterable[Callable[[], None]] | None = None,
) -> None:
    """Render a toolbar with optional action buttons."""

    container = st.container()
    container.markdown("<div class='base-toolbar'>", unsafe_allow_html=True)
    with container.container():
        cols = st.columns([3, 2], gap="small")
        with cols[0]:
            st.markdown(f"<div class='heading-2'>{title}</div>", unsafe_allow_html=True)
            if description:
                st.markdown(f"<div class='body-text'>{description}</div>", unsafe_allow_html=True)
        with cols[1]:
            if actions:
                st.markdown("<div class='base-toolbar__actions'>", unsafe_allow_html=True)
                for render_action in actions:
                    render_action()
                st.markdown("</div>", unsafe_allow_html=True)
    container.markdown("</div>", unsafe_allow_html=True)
