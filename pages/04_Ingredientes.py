import streamlit as st
import pandas as pd

from repos import ingredientes_repo as repo
from services.lookups import fetch_lookup
from services.validators import require_nonempty
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("04 — Ingredientes")

tipo_opts = fetch_lookup("tipo_de_insumo", id_col="id", label_col="nombre")

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_ing"):
    nombre = st.text_input("Nombre")
    tipo_id = dropdown_fk("Tipo de insumo", tipo_opts, key="create_tipo")
    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            nombre = require_nonempty(nombre, "nombre")
            if tipo_id is None:
                raise ValueError("tipo_insumo_id is required (no options).")
            repo.create(nombre, tipo_id)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="nombre", key="pick_ing")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_ing"):
            nombre_e = st.text_input("Nombre", value=row.get("nombre", ""))
            tipo_default = row.get("tipo_insumo_id")
            tipo_id_e = dropdown_fk("Tipo de insumo", tipo_opts, key="edit_tipo")
            ok = st.form_submit_button("Update")
            if ok:
                try:
                    nombre_e = require_nonempty(nombre_e, "nombre")
                    if tipo_id_e is None:
                        raise ValueError("tipo_insumo_id is required (no options).")
                    repo.update(row["id"], nombre_e, tipo_id_e)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_ing", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
