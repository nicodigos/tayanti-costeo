import streamlit as st
import pandas as pd

from repos import recetas_insumo_repo as repo
from services.lookups import fetch_lookup
from services.validators import require_nonempty
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("Recetas General")

cat_opts = fetch_lookup("categoria_receta_insumo", id_col="id", label_col="nombre")

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_ri"):
    nombre = st.text_input("Nombre receta")
    cat_id = dropdown_fk("Categoría", cat_opts, key="ri_cat")
    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            nombre = require_nonempty(nombre, "nombre")
            if cat_id is None:
                raise ValueError("categoria_receta_insumo_id is required (no options).")
            repo.create(nombre, cat_id)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="nombre", key="pick_ri")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_ri"):
            nombre_e = st.text_input("Nombre receta", value=row.get("nombre", ""))
            cat_id_e = dropdown_fk("Categoría", cat_opts, key="ri_cat_e")
            ok = st.form_submit_button("Update")
            if ok:
                try:
                    nombre_e = require_nonempty(nombre_e, "nombre")
                    if cat_id_e is None:
                        raise ValueError("categoria_receta_insumo_id is required (no options).")
                    repo.update(row["id"], nombre_e, cat_id_e)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_ri", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
