import streamlit as st
import pandas as pd
from decimal import Decimal

from repos import receta_componentes_repo as repo
from services.lookups import fetch_componentes_lookup, fetch_rie_lookup, fetch_lookup
from services.validators import require_int, require_decimal_gt
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("07 — Receta Componentes")

# Requires these tables in your DB:
rie_opts = fetch_rie_lookup()
comp_opts = fetch_componentes_lookup()
unidad_opts = fetch_lookup("unidad_de_medida", id_col="id", label_col="nombre")   # must exist

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_rc"):
    rie_id = dropdown_fk("Receta_insumo_especifica", rie_opts, key="c_rie_rc")
    comp_id = dropdown_fk("Componente", comp_opts, key="c_comp_rc")
    uni_id = dropdown_fk("Unidad de medida", unidad_opts, key="c_uni_rc")

    cantidad = st.number_input("Cantidad", min_value=0.0, value=1.0, step=0.1)
    nota = st.text_area("Nota (opcional)")

    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            if rie_id is None or comp_id is None or uni_id is None:
                raise ValueError("receta/componente/unidad are required (missing options).")

            qty = require_decimal_gt(cantidad, "cantidad", Decimal("0"))

            payload = {
                "receta_insumo_especifica_id": require_int(rie_id, "receta_insumo_especifica_id"),
                "componente_id": require_int(comp_id, "componente_id"),
                "unidad_medida_id": require_int(uni_id, "unidad_medida_id"),
                "cantidad": float(qty),
                "nota": nota or None,
            }
            repo.create(payload)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="id", key="pick_rc")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_rc"):
            rie_id_e = dropdown_fk("Receta_insumo_especifica", rie_opts, key="e_rie_rc")
            comp_id_e = dropdown_fk("Componente", comp_opts, key="e_comp_rc")
            uni_id_e = dropdown_fk("Unidad de medida", unidad_opts, key="e_uni_rc")

            cantidad_e = st.number_input("Cantidad", min_value=0.0, value=float(row.get("cantidad", 1.0)), step=0.1)
            nota_e = st.text_area("Nota (opcional)", value=row.get("nota") or "")

            ok = st.form_submit_button("Update")
            if ok:
                try:
                    if rie_id_e is None or comp_id_e is None or uni_id_e is None:
                        raise ValueError("receta/componente/unidad are required (missing options).")

                    qty = require_decimal_gt(cantidad_e, "cantidad", Decimal("0"))

                    payload = {
                        "receta_insumo_especifica_id": require_int(rie_id_e, "receta_insumo_especifica_id"),
                        "componente_id": require_int(comp_id_e, "componente_id"),
                        "unidad_medida_id": require_int(uni_id_e, "unidad_medida_id"),
                        "cantidad": float(qty),
                        "nota": nota_e or None,
                    }
                    repo.update(row["id"], payload)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_rc", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
