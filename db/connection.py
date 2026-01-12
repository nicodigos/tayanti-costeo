import os
import requests
import streamlit as st

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA", "public")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment variables.")

BASE = f"{SUPABASE_URL}/rest/v1"


def _require_login():
    if "session" not in st.session_state or not st.session_state.session:
        # If someone tries to call DB functions without login
        st.error("You must be logged in.")
        st.stop()


def _headers():
    _require_login()
    token = st.session_state.session.access_token

    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation",
    }


def rest_get(table, params=None):
    return requests.get(
        f"{BASE}/{table}",
        headers=_headers(),
        params=params or {},
    )


def rest_post(table, json):
    return requests.post(
        f"{BASE}/{table}",
        headers=_headers(),
        json=json,
    )


def rest_patch(table, row_id, json):
    return requests.patch(
        f"{BASE}/{table}?id=eq.{row_id}",
        headers=_headers(),
        json=json,
    )


def rest_delete(table, row_id):
    return requests.delete(
        f"{BASE}/{table}?id=eq.{row_id}",
        headers=_headers(),
    )
