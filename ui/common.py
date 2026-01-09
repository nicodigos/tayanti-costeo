import streamlit as st

def show_error(e: Exception):
    st.error(str(e))

def confirm_box(key: str, label="Confirm delete?") -> bool:
    return st.checkbox(label, key=key)
