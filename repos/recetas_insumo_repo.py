from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "recetas_insumo"

def list_all():
    r = rest_get(TABLE, {
        "select": "id,nombre,categoria_receta_insumo_id,categoria_receta_insumo(nombre)",
        "order": "nombre"
    })
    r.raise_for_status()
    rows = r.json()

    new_rows = []

    for row in rows:
        new_rows.append({
            "id": row["id"],
            "nombre": row.get("nombre"),
            "categoria": (row.get("categoria_receta_insumo") or {}).get("nombre"),
        })

    return new_rows


def create(nombre, categoria_receta_insumo_id):
    r = rest_post(TABLE, {
        "nombre": nombre,
        "categoria_receta_insumo_id": categoria_receta_insumo_id
    })
    r.raise_for_status()
    return r.json()

def update(row_id, nombre, categoria_receta_insumo_id):
    r = rest_patch(TABLE, row_id, {
        "nombre": nombre,
        "categoria_receta_insumo_id": categoria_receta_insumo_id
    })
    r.raise_for_status()
    return r.json()

def delete(row_id):
    r = rest_delete(TABLE, row_id)
    r.raise_for_status()
