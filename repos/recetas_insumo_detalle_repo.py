from db.connection import rest_get, rest_post, rest_patch, rest_delete

TABLE = "recetas_insumo_detalle"


def list_all():
    r = rest_get(TABLE, {
        "select": (
            "id,receta_especifica_id,proveedor_ingrediente_precios_id,subreceta_especifica_id,"
            "cantidad,unidad_medida_id,orden,nota,"

            # Padre (alias)
            "padre:recetas_insumo_especifica!receta_especifica_id("
                "id,version,recetas_insumo(nombre)"
            "),"

            # Subreceta (alias)
            "sub:recetas_insumo_especifica!subreceta_especifica_id("
                "id,version,recetas_insumo(nombre)"
            "),"

            # Ingrediente específico (PIP) (alias)
            "pip:proveedor_ingrediente_precios!proveedor_ingrediente_precios_id("
                "id,presentacion,costo_presentacion,fecha_vigencia,presentacion_raw,"
                "proveedores(nombre),ingredientes(nombre),unidad_de_medida(nombre)"
            "),"

            # Unidad usada en la receta para 'cantidad'
            "unidad_de_medida(nombre)"
        ),
        "order": "receta_especifica_id.asc,orden.asc,id.asc"
    })
    r.raise_for_status()
    rows = r.json() or []

    new_rows = []
    for row in rows:
        padre = row.get("padre") or {}
        padre_nombre = (padre.get("recetas_insumo") or {}).get("nombre")
        padre_label = f"{padre_nombre} — {padre.get('version')}" if padre_nombre else None

        sub = row.get("sub") or {}
        sub_nombre = (sub.get("recetas_insumo") or {}).get("nombre")
        sub_label = f"{sub_nombre} — {sub.get('version')}" if sub_nombre else None

        pip = row.get("pip") or {}
        pip_label = None
        if pip:
            prov = (pip.get("proveedores") or {}).get("nombre")
            ing = (pip.get("ingredientes") or {}).get("nombre")
            uni = (pip.get("unidad_de_medida") or {}).get("nombre")
            pres = pip.get("presentacion")
            cost = pip.get("costo_presentacion")
            vig = pip.get("fecha_vigencia")
            pip_label = f"{ing} · {prov} · {uni} · {pres} · ${cost} · {vig}"

        new_rows.append({
            "id": row["id"],
            "receta": padre_label,
            "ingrediente_especifico": pip_label,
            "subreceta": sub_label,
            "cantidad": row.get("cantidad"),
            "unidad": (row.get("unidad_de_medida") or {}).get("nombre"),
            "orden": row.get("orden"),
            "nota": row.get("nota"),
        })

    return new_rows


def create(payload):
    r = rest_post(TABLE, payload)
    r.raise_for_status()
    return r.json()


def update(row_id, payload):
    r = rest_patch(TABLE, row_id, payload)
    r.raise_for_status()
    return r.json()


def delete(row_id):
    r = rest_delete(TABLE, row_id)
    r.raise_for_status()
