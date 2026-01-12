import streamlit as st
import pandas as pd
from decimal import Decimal

from repos import proveedor_ingrediente_precios_repo as repo
from services.lookups import fetch_lookup
from services.validators import require_int, require_decimal_gt, require_decimal_gte
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("Proveedor · Ingrediente · Precios")

# These tables must exist in your DB:
proveedor_opts = fetch_lookup("proveedores", id_col="id", label_col="nombre")  # must exist
ingrediente_opts = fetch_lookup("ingredientes", id_col="id", label_col="nombre")
unidad_opts = fetch_lookup("unidad_de_medida", id_col="id", label_col="nombre")  # must exist

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_pip"):
    prov_id = dropdown_fk("Proveedor", proveedor_opts, key="c_prov")
    ing_id = dropdown_fk("Ingrediente", ingrediente_opts, key="c_ing")
    uni_id = dropdown_fk("Unidad de medida", unidad_opts, key="c_uni")

    presentacion = st.number_input("Presentación", min_value=0.0, value=1.0, step=0.1)
    costo = st.number_input("Costo presentación", min_value=0.0, value=0.0, step=1.0)
    fecha = st.date_input("Fecha vigencia")
    raw = st.text_input("Presentación raw (opcional)")

    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            if prov_id is None or ing_id is None or uni_id is None:
                raise ValueError("Proveedor/Ingrediente/Unidad are required (missing options).")

            p = require_decimal_gt(presentacion, "presentacion", Decimal("0"))
            c = require_decimal_gte(costo, "costo_presentacion", Decimal("0"))

            payload = {
                "proveedor_id": require_int(prov_id, "proveedor_id"),
                "ingrediente_id": require_int(ing_id, "ingrediente_id"),
                "unidad_medida_id": require_int(uni_id, "unidad_medida_id"),
                "presentacion": float(p),
                "costo_presentacion": float(c),
                "fecha_vigencia": str(fecha),
                "presentacion_raw": raw or None,
            }
            repo.create(payload)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="id", key="pick_pip")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_pip"):
            prov_id_e = dropdown_fk("Proveedor", proveedor_opts, key="e_prov")
            ing_id_e = dropdown_fk("Ingrediente", ingrediente_opts, key="e_ing")
            uni_id_e = dropdown_fk("Unidad de medida", unidad_opts, key="e_uni")

            presentacion_e = st.number_input("Presentación", min_value=0.0, value=float(row.get("presentacion", 1.0)), step=0.1)
            costo_e = st.number_input("Costo presentación", min_value=0.0, value=float(row.get("costo_presentacion", 0.0)), step=1.0)
            fecha_e = st.date_input("Fecha vigencia", value=pd.to_datetime(row.get("fecha_vigencia")).date() if row.get("fecha_vigencia") else None)
            raw_e = st.text_input("Presentación raw (opcional)", value=row.get("presentacion_raw") or "")

            ok = st.form_submit_button("Update")
            if ok:
                try:
                    if prov_id_e is None or ing_id_e is None or uni_id_e is None:
                        raise ValueError("Proveedor/Ingrediente/Unidad are required (missing options).")

                    p = require_decimal_gt(presentacion_e, "presentacion", Decimal("0"))
                    c = require_decimal_gte(costo_e, "costo_presentacion", Decimal("0"))

                    payload = {
                        "proveedor_id": require_int(prov_id_e, "proveedor_id"),
                        "ingrediente_id": require_int(ing_id_e, "ingrediente_id"),
                        "unidad_medida_id": require_int(uni_id_e, "unidad_medida_id"),
                        "presentacion": float(p),
                        "costo_presentacion": float(c),
                        "fecha_vigencia": str(fecha_e),
                        "presentacion_raw": raw_e or None,
                    }
                    repo.update(row["id"], payload)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_pip", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
