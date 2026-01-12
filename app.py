import streamlit as st
from db.healthcheck import supabase_healthcheck


st.set_page_config(page_title="Recetas CRUD", layout="wide")

st.title("Tayanti Costeo")

ok, msg = supabase_healthcheck()
if ok:
    st.success(msg)
else:
    st.error(msg)
    st.stop()

st.markdown(
    """
Use the pages on the left sidebar to manage each table.
"""
)
