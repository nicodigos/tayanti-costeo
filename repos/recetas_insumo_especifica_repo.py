from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "recetas_insumo_especifica"

def list_all():
    r = rest_get(TABLE, {
        "select": "id,version,cantidad,recetas_insumo(nombre),unidad_de_medida(nombre),chef_responsable(nombre)",
        "order": "id.desc"
    })
    r.raise_for_status()
    rows = r.json()

    new_rows = []

    for row in rows:
        new_rows.append({
            "id": row["id"],
            "receta": (row.get("recetas_insumo") or {}).get("nombre"),
            "version": row.get("version"),
            "cantidad": row.get("cantidad"),
            "unidad": (row.get("unidad_de_medida") or {}).get("nombre"),
            "chef": (row.get("chef_responsable") or {}).get("nombre"),
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
