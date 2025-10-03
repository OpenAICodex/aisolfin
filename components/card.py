"""Card layout component."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterable, Optional

import streamlit as st


@contextmanager
def card(
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    actions: Optional[Iterable[Callable[[], None]]] = None,
    flush: bool = False,
):
    """Render a themed card container.

    Parameters
    ----------
    title:
        Optional heading text rendered using the heading-3 style.
    subtitle:
        Supporting copy rendered underneath the title.
    actions:
        Iterable of callables that render Streamlit elements aligned to the
        right of the card header.
    flush:
        Removes internal padding when ``True`` to support tables and charts.
    """

    wrapper = st.container()
    card_classes = ["base-card"]
    if flush:
        card_classes.append("base-card--flush")

    wrapper.markdown(
        f"<div class='{' '.join(card_classes)}'>",
        unsafe_allow_html=True,
    )
    body = wrapper.container()

    if title or subtitle or actions:
        header = body.container()
        cols = header.columns([1, 1], gap="small")
        with cols[0]:
            if title:
                st.markdown(f"<div class='heading-3'>{title}</div>", unsafe_allow_html=True)
            if subtitle:
                st.markdown(f"<div class='body-text'>{subtitle}</div>", unsafe_allow_html=True)
        with cols[1]:
            if actions:
                st.markdown("<div class='base-toolbar__actions'>", unsafe_allow_html=True)
                for render_action in actions:
                    render_action()
                st.markdown("</div>", unsafe_allow_html=True)

    content = body.container()
    try:
        yield content
    finally:
        wrapper.markdown("</div>", unsafe_allow_html=True)
