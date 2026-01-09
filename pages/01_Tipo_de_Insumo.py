import streamlit as st
import pandas as pd

from repos import tipo_de_insumo_repo as repo
from services.validators import require_nonempty, require_percentage_0_100
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id

st.title("01 — Tipo de Insumo")

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_tipo"):
    nombre = st.text_input("Nombre")
    merma = st.number_input("Merma (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            nombre = require_nonempty(nombre, "nombre")
            merma = require_percentage_0_100(merma, "merma")
            repo.create(nombre, merma)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="nombre", key="pick_tipo")
if row:
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Edit")
        with st.form("edit_tipo"):
            nombre_e = st.text_input("Nombre", value=row["nombre"])
            merma_e = st.number_input("Merma (%)", min_value=0.0, max_value=100.0, value=float(row["merma"]), step=0.5)
            ok = st.form_submit_button("Update")
            if ok:
                try:
                    nombre_e = require_nonempty(nombre_e, "nombre")
                    merma_e = require_percentage_0_100(merma_e, "merma")
                    repo.update(row["id"], nombre_e, merma_e)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        st.caption("Delete")
        if confirm_box("confirm_del_tipo", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
