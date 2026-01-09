import streamlit as st
import pandas as pd

from repos import componentes_repo as repo
from services.lookups import fetch_pip_lookup, fetch_rie_lookup
from services.validators import require_nonempty, require_int
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("06 — Componentes")

# Lookups needed
pip_opts = fetch_pip_lookup()
rie_opts = fetch_rie_lookup()

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

TIPOS = ["COMPRA_INGREDIENTE", "RECETA"]

st.divider()
st.subheader("Create")
with st.form("create_comp"):
    tipo = st.selectbox("Tipo", TIPOS, index=0)
    nombre = st.text_input("Nombre")

    pip_id = None
    rie_id = None

    if tipo == "COMPRA_INGREDIENTE":
        pip_id = dropdown_fk("Proveedor_Ingrediente_Precios", pip_opts, key="c_pip")
    else:
        rie_id = dropdown_fk("Receta_Insumo_Especifica", rie_opts, key="c_rie")

    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            nombre = require_nonempty(nombre, "nombre")

            payload = {"tipo": tipo, "nombre": nombre}
            if tipo == "COMPRA_INGREDIENTE":
                if pip_id is None:
                    raise ValueError("proveedor_ingrediente_precios_id is required.")
                payload["proveedor_ingrediente_precios_id"] = require_int(pip_id, "proveedor_ingrediente_precios_id")
                payload["receta_insumo_especifica_id"] = None
            else:
                if rie_id is None:
                    raise ValueError("receta_insumo_especifica_id is required.")
                payload["receta_insumo_especifica_id"] = require_int(rie_id, "receta_insumo_especifica_id")
                payload["proveedor_ingrediente_precios_id"] = None

            repo.create(payload)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="nombre", key="pick_comp")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_comp"):
            tipo_e = st.selectbox("Tipo", TIPOS, index=TIPOS.index(row.get("tipo", "COMPRA_INGREDIENTE")))
            nombre_e = st.text_input("Nombre", value=row.get("nombre", ""))

            pip_id_e = None
            rie_id_e = None
            if tipo_e == "COMPRA_INGREDIENTE":
                pip_id_e = dropdown_fk("Proveedor_Ingrediente_Precios", pip_opts, key="e_pip")
            else:
                rie_id_e = dropdown_fk("Receta_Insumo_Especifica", rie_opts, key="e_rie")

            ok = st.form_submit_button("Update")
            if ok:
                try:
                    nombre_e = require_nonempty(nombre_e, "nombre")

                    payload = {"tipo": tipo_e, "nombre": nombre_e}
                    if tipo_e == "COMPRA_INGREDIENTE":
                        if pip_id_e is None:
                            raise ValueError("proveedor_ingrediente_precios_id is required.")
                        payload["proveedor_ingrediente_precios_id"] = require_int(pip_id_e, "proveedor_ingrediente_precios_id")
                        payload["receta_insumo_especifica_id"] = None
                    else:
                        if rie_id_e is None:
                            raise ValueError("receta_insumo_especifica_id is required.")
                        payload["receta_insumo_especifica_id"] = require_int(rie_id_e, "receta_insumo_especifica_id")
                        payload["proveedor_ingrediente_precios_id"] = None

                    repo.update(row["id"], payload)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_comp", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
