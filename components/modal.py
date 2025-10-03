"""Modal component."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Optional
import streamlit as st


@contextmanager
def modal(visible: bool, title: Optional[str] = None):
    """Render a modal dialog when ``visible`` is ``True``.

    Parameters
    ----------
    visible:
        Toggles the modal visibility. When ``False`` the context yields ``None``.
    title:
        Optional string rendered at the top of the modal body.
    """

    if not visible:
        yield None
        return

    placeholder = st.empty()
    placeholder.markdown("<div class='base-modal__overlay'>", unsafe_allow_html=True)
    content_container = placeholder.container()
    content_container.markdown("<div class='base-modal__content'>", unsafe_allow_html=True)
    if title:
        content_container.markdown(f"<div class='heading-3'>{title}</div>", unsafe_allow_html=True)
    body = content_container.container()
    try:
        yield body
    finally:
        content_container.markdown("</div>", unsafe_allow_html=True)
        placeholder.markdown("</div>", unsafe_allow_html=True)
