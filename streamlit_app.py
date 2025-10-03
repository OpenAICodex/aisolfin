"""Streamlit app with Supabase magic link authentication."""
from __future__ import annotations

import os
from typing import Optional

import streamlit as st
from supabase import Client, create_client


def get_supabase_client() -> Client:
    """Create a Supabase client using Streamlit secrets or environment variables."""
    supabase_url: Optional[str] = st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None
    supabase_key: Optional[str] = st.secrets.get("SUPABASE_ANON_KEY") if hasattr(st, "secrets") else None

    # Fall back to environment variables when developing locally.
    supabase_url = supabase_url or os.getenv("SUPABASE_URL")
    supabase_key = supabase_key or os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        st.error(
            "Supabase credentials are missing. Set SUPABASE_URL and SUPABASE_ANON_KEY "
            "in Streamlit secrets or environment variables."
        )
        st.stop()

    return create_client(supabase_url, supabase_key)


def ensure_session_from_query_params(client: Client) -> None:
    """Populate the Supabase session when tokens are supplied via query params."""
    params = st.experimental_get_query_params()
    access_token = params.get("access_token", [None])[0]
    refresh_token = params.get("refresh_token", [None])[0]

    if access_token and refresh_token:
        client.auth.set_session(access_token, refresh_token)
        user_response = client.auth.get_user(access_token)
        if user_response.user:
            st.session_state["user"] = user_response.user
        # Clear sensitive query params from the URL once they are consumed.
        st.experimental_set_query_params()


def main() -> None:
    st.set_page_config(page_title="Welcome", page_icon="👋")

    st.title("Welcome to the AI Solutions Portal 👋")
    st.write(
        "We're glad you're here! Please sign in to continue. You'll receive a secure "
        "magic link by email—no password required."
    )

    client = get_supabase_client()
    ensure_session_from_query_params(client)

    if "user" in st.session_state and st.session_state["user"] is not None:
        user = st.session_state["user"]
        st.success(f"You are logged in as {user.email}.")

        if st.button("Log out"):
            client.auth.sign_out()
            st.session_state.pop("user", None)
            st.experimental_rerun()
        return

    st.subheader("Sign in with a magic link")
    email = st.text_input("Email address", placeholder="you@example.com")

    if st.button("Send me a magic link", type="primary"):
        if not email:
            st.warning("Please enter your email address.")
        else:
            redirect_url: Optional[str] = None
            if hasattr(st, "secrets"):
                redirect_url = st.secrets.get("APP_URL")
            redirect_url = redirect_url or os.getenv("APP_URL")

            otp_options = {"email_redirect_to": redirect_url} if redirect_url else None
            try:
                response = client.auth.sign_in_with_otp({"email": email, "options": otp_options})
            except Exception as exc:  # pragma: no cover - Streamlit UI feedback
                st.error(f"Unable to send magic link: {exc}")
            else:
                if getattr(response, "user", None) is not None or getattr(response, "session", None) is not None:
                    st.info(
                        "If that email is registered, a magic link has been sent. "
                        "Please check your inbox and return via the link to finish signing in."
                    )
                else:
                    st.warning(
                        "Request received. If you do not receive an email shortly, double-check "
                        "the address and try again."
                    )


if __name__ == "__main__":
    main()
