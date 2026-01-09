import streamlit as st
import pandas as pd
from decimal import Decimal

from repos import recetas_insumo_especifica_repo as repo
from services.lookups import fetch_lookup
from services.validators import require_nonempty, require_int, require_decimal_gt
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("09 — Versiones de receta (recetas_insumo_especifica)")

rec_opts = fetch_lookup("recetas_insumo", id_col="id", label_col="nombre")
uni_opts = fetch_lookup("unidad_de_medida", id_col="id", label_col="nombre")
chef_opts = fetch_lookup("chef_responsable", id_col="id", label_col="nombre")

rows = repo.list_all()
st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Create")
with st.form("create_rie"):
    rec_id = dropdown_fk("Receta base", rec_opts, key="c_rie_rec")
    version = st.text_input("Version (ej: Version octubre 2025 - cocina central)")
    uni_id = dropdown_fk("Unidad de medida", uni_opts, key="c_rie_uni")
    chef_id = dropdown_fk("Chef responsable", chef_opts, key="c_rie_chef")
    cantidad = st.number_input("Cantidad", min_value=0.0, value=1.0, step=0.1)

    submitted = st.form_submit_button("Create")
    if submitted:
        try:
            if rec_id is None or uni_id is None or chef_id is None:
                raise ValueError("recetas_insumo / unidad / chef are required (missing options).")

            version = require_nonempty(version, "version")
            qty = require_decimal_gt(cantidad, "cantidad", Decimal("0"))

            payload = {
                "recetas_insumo_id": require_int(rec_id, "recetas_insumo_id"),
                "version": version,
                "unidad_medida_id": require_int(uni_id, "unidad_medida_id"),
                "chef_responsable_id": require_int(chef_id, "chef_responsable_id"),
                "cantidad": float(qty),
            }
            repo.create(payload)
            st.success("Created.")
            st.rerun()
        except Exception as e:
            show_error(e)

st.divider()
st.subheader("Edit / Delete")
row = pick_row_by_id("Pick a row", rows, id_key="id", display_key="version", key="pick_rie")
if row:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("edit_rie"):
            rec_id_e = dropdown_fk("Receta base", rec_opts, key="e_rie_rec")
            version_e = st.text_input("Version", value=row.get("version", ""))
            uni_id_e = dropdown_fk("Unidad de medida", uni_opts, key="e_rie_uni")
            chef_id_e = dropdown_fk("Chef responsable", chef_opts, key="e_rie_chef")
            cantidad_e = st.number_input("Cantidad", min_value=0.0, value=float(row.get("cantidad", 1.0)), step=0.1)

            ok = st.form_submit_button("Update")
            if ok:
                try:
                    if rec_id_e is None or uni_id_e is None or chef_id_e is None:
                        raise ValueError("recetas_insumo / unidad / chef are required (missing options).")

                    version_e = require_nonempty(version_e, "version")
                    qty = require_decimal_gt(cantidad_e, "cantidad", Decimal("0"))

                    payload = {
                        "recetas_insumo_id": require_int(rec_id_e, "recetas_insumo_id"),
                        "version": version_e,
                        "unidad_medida_id": require_int(uni_id_e, "unidad_medida_id"),
                        "chef_responsable_id": require_int(chef_id_e, "chef_responsable_id"),
                        "cantidad": float(qty),
                    }
                    repo.update(row["id"], payload)
                    st.success("Updated.")
                    st.rerun()
                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("confirm_del_rie", "I understand this will delete the row"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
