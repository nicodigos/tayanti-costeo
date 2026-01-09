import streamlit as st
import pandas as pd

from repos import categoria_receta_insumo_repo as repo
from services.validators import require_nonempty
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id

st.title("03 — Categoría Receta Insumo")

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_cat"):
    nombre = st.text_input("Nombre")
    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            nombre = require_nonempty(nombre, "nombre")
            repo.create(nombre)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="nombre", key="pick_cat")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_cat"):
            nombre_e = st.text_input("Nombre", value=row["nombre"])
            ok = st.form_submit_button("Update")
            if ok:
                try:
                    nombre_e = require_nonempty(nombre_e, "nombre")
                    repo.update(row["id"], nombre_e)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_cat", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
