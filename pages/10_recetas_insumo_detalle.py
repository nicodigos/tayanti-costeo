import streamlit as st
import pandas as pd
from decimal import Decimal

from repos import recetas_insumo_detalle_repo as repo
from services.lookups import fetch_lookup, fetch_pip_lookup, fetch_rie_lookup
from services.validators import require_int, require_decimal_gt
from ui.common import show_error, confirm_box
from ui.widgets import pick_row_by_id, dropdown_fk

st.title("10 — Recetas · Insumo · Detalle")

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

# ------------------------------------------------------
# Helpers: decide qué ignorar si ambos están "seleccionados"
# ------------------------------------------------------
def decide_component(pip_key: str, sub_key: str, prefer: str = "pip"):
    """
    Returns (pip_id_to_send, sub_id_to_send)

    Strategy:
    - If we detect which one changed vs last snapshot, we keep the changed one and ignore the other.
    - If we can't detect, fall back to `prefer` ("pip" or "sub").
    """
    pip_id = st.session_state.get(pip_key)
    sub_id = st.session_state.get(sub_key)

    prev_pip = st.session_state.get(pip_key + "__prev")
    prev_sub = st.session_state.get(sub_key + "__prev")

    pip_changed = (prev_pip is not None and pip_id != prev_pip)
    sub_changed = (prev_sub is not None and sub_id != prev_sub)

    # Update snapshots for next run
    st.session_state[pip_key + "__prev"] = pip_id
    st.session_state[sub_key + "__prev"] = sub_id

    # If we can tell what changed, keep that and ignore the other
    if sub_changed and not pip_changed:
        return (None, sub_id)
    if pip_changed and not sub_changed:
        return (pip_id, None)

    # If both changed or neither changed, use priority
    if prefer == "sub":
        return (None, sub_id)
    return (pip_id, None)  # default: prefer pip


# ======================================================
# CREATE
# ======================================================
st.divider()
st.subheader("Create")

with st.form("create_detalle"):
    receta_padre_id = dropdown_fk("Receta (con versión)", recetas_especifica_opts, key="det_c_padre")

    col1, col2 = st.columns(2)
    with col1:
        pip_id = dropdown_fk("Ingrediente (específico: proveedor/precio)", pip_opts, key="det_c_pip")
    with col2:
        subreceta_id = dropdown_fk("Subreceta (con versión)", recetas_especifica_opts, key="det_c_sub")

    cantidad = st.number_input("Cantidad", min_value=0.0, value=1.0)
    unidad_id = dropdown_fk("Unidad", unidad_opts, key="det_c_uni")
    nota = st.text_input("Nota")

    submitted = st.form_submit_button("Create")

    if submitted:
        try:
            if not receta_padre_id:
                raise ValueError("Receta (con versión) requerida.")
            if not unidad_id:
                raise ValueError("Unidad requerida.")

            q = require_decimal_gt(cantidad, "cantidad", Decimal("0"))

            # Decide qué mandar (ignora uno automáticamente)
            pip_to_send, sub_to_send = decide_component("det_c_pip", "det_c_sub", prefer="pip")

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
        with st.form("edit_detalle"):
            receta_padre_id_e = dropdown_fk("Receta (con versión)", recetas_especifica_opts, key="det_e_padre")

            c1, c2 = st.columns(2)
            with c1:
                pip_id_e = dropdown_fk("Ingrediente (específico: proveedor/precio)", pip_opts, key="det_e_pip")
            with c2:
                subreceta_id_e = dropdown_fk("Subreceta (con versión)", recetas_especifica_opts, key="det_e_sub")

            cantidad_e = st.number_input("Cantidad", min_value=0.0, value=float(row.get("cantidad") or 1.0))
            unidad_id_e = dropdown_fk("Unidad", unidad_opts, key="det_e_uni")
            nota_e = st.text_input("Nota", value=row.get("nota") or "")

            submitted_e = st.form_submit_button("Update")

            if submitted_e:
                try:
                    if not receta_padre_id_e:
                        raise ValueError("Receta (con versión) requerida.")
                    if not unidad_id_e:
                        raise ValueError("Unidad requerida.")

                    q = require_decimal_gt(cantidad_e, "cantidad", Decimal("0"))

                    # Decide qué mandar (ignora uno automáticamente)
                    pip_to_send_e, sub_to_send_e = decide_component("det_e_pip", "det_e_sub", prefer="pip")

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
