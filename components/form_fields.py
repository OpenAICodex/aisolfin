"""Form field wrappers with consistent styling."""
from __future__ import annotations

from typing import Sequence, TypeVar

import streamlit as st

T = TypeVar("T")


def input_field(
    key: str,
    label: str,
    value: str | None = None,
    placeholder: str | None = None,
    help_text: str | None = None,
    error: str | None = None,
    disabled: bool = False,
) -> str:
    """Render a text input with Base44 styling."""

    wrapper = st.container()
    wrapper.markdown("<div class='base-input'>", unsafe_allow_html=True)
    if label:
        wrapper.markdown(f"<label class='base-input__label' for='{key}'>{label}</label>", unsafe_allow_html=True)

    result = wrapper.text_input(
        label="",
        value=value if value is not None else "",
        key=key,
        placeholder=placeholder,
        disabled=disabled,
        label_visibility="collapsed",
    )

    if error:
        wrapper.markdown(f"<div class='base-input__error'>{error}</div>", unsafe_allow_html=True)
    elif help_text:
        wrapper.markdown(f"<div class='base-input__helper'>{help_text}</div>", unsafe_allow_html=True)

    wrapper.markdown("</div>", unsafe_allow_html=True)
    return result


def select_field(
    key: str,
    label: str,
    options: Sequence[T],
    index: int | None = None,
    format_func = str,
    help_text: str | None = None,
    error: str | None = None,
    disabled: bool = False,
) -> T:
    """Render a select input with Base44 styling."""

    wrapper = st.container()
    wrapper.markdown("<div class='base-select'>", unsafe_allow_html=True)
    if label:
        wrapper.markdown(f"<label class='base-select__label' for='{key}'>{label}</label>", unsafe_allow_html=True)

    result = wrapper.selectbox(
        label="",
        options=options,
        index=index,
        key=key,
        format_func=format_func,
        disabled=disabled,
        label_visibility="collapsed",
    )

    if error:
        wrapper.markdown(f"<div class='base-select__error'>{error}</div>", unsafe_allow_html=True)
    elif help_text:
        wrapper.markdown(f"<div class='base-select__helper'>{help_text}</div>", unsafe_allow_html=True)

    wrapper.markdown("</div>", unsafe_allow_html=True)
    return result
