"""Authentication helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


@dataclass
class User:
    email: str
    name: str


SESSION_KEY = "current_user"


def login(email: str, password: str) -> User:
    """Mock authentication implementation."""

    if "@" not in email or not password:
        raise ValueError("Invalid credentials")
    user = User(email=email, name=email.split("@")[0].title())
    st.session_state[SESSION_KEY] = user
    return user


def logout() -> None:
    st.session_state.pop(SESSION_KEY, None)


def current_user() -> Optional[User]:
    return st.session_state.get(SESSION_KEY)
