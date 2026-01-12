import streamlit as st
import pandas as pd
from decimal import Decimal

from repos import recetas_insumo_detalle_repo as repo
from services.lookups import fetch_lookup, fetch_pip_lookup, fetch_rie_lookup
from services.validators import require_int, require_decimal_gt
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("Cruce de Recetas e Insumos")

# -----------------------------
# Lookups
# -----------------------------
recetas_especifica_opts = fetch_rie_lookup()   # (id, label) recetas_insumo_especifica
pip_opts = fetch_pip_lookup()                 # (id, label) proveedor_ingrediente_precios
unidad_opts = fetch_lookup("unidad_de_medida", id_col="id", label_col="nombre")

# -----------------------------
# Data
# -----------------------------
rows = repo.list_all()

st.subheader("Current rows")
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ======================================================
# CREATE
# ======================================================
st.divider()
st.subheader("Create")

# ✅ Outside the form: choose which component UI to load
component_type_create = st.radio(
    "Component type",
    ["Ingrediente", "Subreceta"],
    horizontal=True,
    key="det_c_component_type"
)

use_subreceta_create = component_type_create == "Subreceta"

with st.form("create_detalle"):
    receta_padre_id = dropdown_fk("Receta (con versión)", recetas_especifica_opts, key="det_c_padre")

    # ✅ Inside form: render ONLY ONE picker depending on checkbox
    if use_subreceta_create:
        subreceta_id = dropdown_fk("Subreceta (con versión)", recetas_especifica_opts, key="det_c_sub")
        pip_id = None
    else:
        pip_id = dropdown_fk("Ingrediente (específico: proveedor/precio)", pip_opts, key="det_c_pip")
        subreceta_id = None

    cantidad = st.number_input("Cantidad", min_value=0.0, value=1.0, key="det_c_cantidad")
    unidad_id = dropdown_fk("Unidad", unidad_opts, key="det_c_uni")
    nota = st.text_input("Nota", key="det_c_nota")

    submitted = st.form_submit_button("Create")

    if submitted:
        try:
            if not receta_padre_id:
                raise ValueError("Receta (con versión) requerida.")
            if not unidad_id:
                raise ValueError("Unidad requerida.")

            q = require_decimal_gt(cantidad, "cantidad", Decimal("0"))

            # ✅ Enforce exactly one component
            if use_subreceta_create:
                if not subreceta_id:
                    raise ValueError("Subreceta requerida.")
                pip_to_send, sub_to_send = (None, subreceta_id)
            else:
                if not pip_id:
                    raise ValueError("Ingrediente requerido.")
                pip_to_send, sub_to_send = (pip_id, None)

            payload = {
                "receta_especifica_id": require_int(receta_padre_id, "receta_especifica_id"),
                "proveedor_ingrediente_precios_id": require_int(pip_to_send, "proveedor_ingrediente_precios_id") if pip_to_send is not None else None,
                "subreceta_especifica_id": require_int(sub_to_send, "subreceta_especifica_id") if sub_to_send is not None else None,
                "cantidad": float(q),
                "unidad_medida_id": require_int(unidad_id, "unidad_medida_id"),
                "nota": nota or None,
            }

            repo.create(payload)
            st.success("Created.")
            st.rerun()

        except Exception as e:
            show_error(e)


# ======================================================
# EDIT / DELETE
# ======================================================
st.divider()
st.subheader("Edit / Delete")

row = pick_row_by_id("Pick row", rows, id_key="id", display_key="id", key="det_pick")

if row:
    col1, col2 = st.columns(2)

    with col1:
        # ✅ Outside the form: choose which component editor to load
        # Initialize default based on the existing row:
        row_has_sub = bool(row.get("subreceta_especifica_id"))
        use_subreceta_edit = st.checkbox(
            "Edit as subrecipe (otherwise ingredient)",
            value=row_has_sub,
            key="det_e_use_sub"
        )

        with st.form("edit_detalle"):
            receta_padre_id_e = dropdown_fk("Receta (con versión)", recetas_especifica_opts, key="det_e_padre")

            # ✅ Inside form: render ONLY ONE picker depending on checkbox
            if use_subreceta_edit:
                subreceta_id_e = dropdown_fk("Subreceta (con versión)", recetas_especifica_opts, key="det_e_sub")
                pip_id_e = None
            else:
                pip_id_e = dropdown_fk("Ingrediente (específico: proveedor/precio)", pip_opts, key="det_e_pip")
                subreceta_id_e = None

            cantidad_e = st.number_input(
                "Cantidad",
                min_value=0.0,
                value=float(row.get("cantidad") or 1.0),
                key="det_e_cantidad"
            )
            unidad_id_e = dropdown_fk("Unidad", unidad_opts, key="det_e_uni")
            nota_e = st.text_input("Nota", value=row.get("nota") or "", key="det_e_nota")

            submitted_e = st.form_submit_button("Update")

            if submitted_e:
                try:
                    if not receta_padre_id_e:
                        raise ValueError("Receta (con versión) requerida.")
                    if not unidad_id_e:
                        raise ValueError("Unidad requerida.")

                    q = require_decimal_gt(cantidad_e, "cantidad", Decimal("0"))

                    # ✅ Enforce exactly one component
                    if use_subreceta_edit:
                        if not subreceta_id_e:
                            raise ValueError("Subreceta requerida.")
                        pip_to_send_e, sub_to_send_e = (None, subreceta_id_e)
                    else:
                        if not pip_id_e:
                            raise ValueError("Ingrediente requerido.")
                        pip_to_send_e, sub_to_send_e = (pip_id_e, None)

                    payload = {
                        "receta_especifica_id": require_int(receta_padre_id_e, "receta_especifica_id"),
                        "proveedor_ingrediente_precios_id": require_int(pip_to_send_e, "proveedor_ingrediente_precios_id") if pip_to_send_e is not None else None,
                        "subreceta_especifica_id": require_int(sub_to_send_e, "subreceta_especifica_id") if sub_to_send_e is not None else None,
                        "cantidad": float(q),
                        "unidad_medida_id": require_int(unidad_id_e, "unidad_medida_id"),
                        "nota": nota_e or None,
                    }

                    repo.update(row["id"], payload)
                    st.success("Updated.")
                    st.rerun()

                except Exception as e:
                    show_error(e)

    with col2:
        if confirm_box("det_confirm_del", "I understand this will delete this component"):
            if st.button("Delete", type="primary"):
                try:
                    repo.delete(row["id"])
                    st.success("Deleted.")
                    st.rerun()
                except Exception as e:
                    show_error(e)
