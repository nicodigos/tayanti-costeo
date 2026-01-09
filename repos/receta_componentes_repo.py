from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "receta_componentes"

def list_all():
    r = rest_get(TABLE, {
        "select": "id,cantidad,nota,componentes(nombre,tipo),unidad_de_medida(nombre)",
        "order": "id.desc"
    })
    r.raise_for_status()
    rows = r.json()

    new_rows = []

    for row in rows:
        new_rows.append({
            "id": row["id"],
            "componente": f'{(row.get("componentes") or {}).get("nombre")} ({(row.get("componentes") or {}).get("tipo")})',
            "cantidad": row.get("cantidad"),
            "unidad": (row.get("unidad_de_medida") or {}).get("nombre"),
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
