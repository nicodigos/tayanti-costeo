from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "ingredientes"

def list_all():
    r = rest_get(TABLE, {
        "select": "id,nombre,tipo_insumo_id,tipo_de_insumo(nombre)",
        "order": "nombre"
    })
    r.raise_for_status()
    rows = r.json()

    new_rows = []

    for row in rows:
        new_rows.append({
            "id": row["id"],
            "nombre": row.get("nombre"),
            "tipo_insumo": (row.get("tipo_de_insumo") or {}).get("nombre")
        })

    return new_rows


def create(nombre, tipo_insumo_id):
    r = rest_post(TABLE, {"nombre": nombre, "tipo_insumo_id": tipo_insumo_id})
    r.raise_for_status()
    return r.json()

def update(row_id, nombre, tipo_insumo_id):
    r = rest_patch(TABLE, row_id, {"nombre": nombre, "tipo_insumo_id": tipo_insumo_id})
    r.raise_for_status()
    return r.json()

def delete(row_id):
    r = rest_delete(TABLE, row_id)
    r.raise_for_status()
