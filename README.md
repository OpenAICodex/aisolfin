# Streamlit Supabase Magic Link Demo

This repository contains a minimal [Streamlit](https://streamlit.io/) app that authenticates
users with [Supabase Auth](https://supabase.com/auth) using passwordless magic links.

## Prerequisites

1. Create a Supabase project and enable **Email OTP** in the Authentication settings.
2. Retrieve the project URL and the anon public API key from the Supabase dashboard.
3. Store these credentials for the app to use:
   - When deploying on Streamlit Cloud, add them to `Secrets` as `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
   - When running locally, export them as environment variables or create a `.streamlit/secrets.toml` file.
4. (Optional) Set `APP_URL` to the public URL of your deployment so Supabase knows where to send
   users after they click the magic link.

```toml
# .streamlit/secrets.toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "public-anon-key"
# Optional: where Supabase should redirect after the user confirms the email
APP_URL = "https://your-app.streamlit.app"
```

## Running locally

Install dependencies and launch the Streamlit development server:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

After entering your email address, Supabase will send a magic link. The link will redirect
back to the application with a session token that completes the sign-in flow.
