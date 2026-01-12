import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()


from db.healthcheck import supabase_healthcheck  # should use user JWT (not service role)

# -----------------------------
# Page
# -----------------------------
st.set_page_config(page_title="Recetas CRUD", layout="wide")
st.title("Tayanti Costeo")

# -----------------------------
# Supabase client for AUTH
# -----------------------------
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY"),
)

# -----------------------------
# Session state
# -----------------------------
if "session" not in st.session_state:
    st.session_state.session = None
if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# Login gate
# -----------------------------
if not st.session_state.session:
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 3])
    with col1:
        login_clicked = st.button("Login", use_container_width=True)

    if login_clicked:
        try:
            res = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if res.session and res.user:
                st.session_state.session = res.session
                st.session_state.user = res.user
                st.rerun()
            else:
                st.error("Invalid credentials.")
        except Exception:
            st.error("Invalid credentials.")

    st.stop()

# -----------------------------
# Header + Logout
# -----------------------------
left, right = st.columns([6, 1])
with left:
    st.caption(f"Logged in as: {st.session_state.user.email}")
with right:
    if st.button("Logout", use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.session = None
        st.session_state.user = None
        st.rerun()

# -----------------------------
# Healthcheck (authenticated)
# -----------------------------
ok, msg = supabase_healthcheck()
if ok:
    st.success(msg)
else:
    st.error(msg)
    st.stop()

st.markdown("Use the pages on the left sidebar to manage each table.")
