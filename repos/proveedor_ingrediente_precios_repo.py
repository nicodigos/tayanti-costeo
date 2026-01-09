from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "proveedor_ingrediente_precios"
def list_all():
    r = rest_get(TABLE, {
        "select": (
            "id,proveedor_id,ingrediente_id,unidad_medida_id,"
            "presentacion,costo_presentacion,fecha_vigencia,presentacion_raw,"
            "proveedores(nombre),ingredientes(nombre),unidad_de_medida(nombre)"
        ),
        "order": "fecha_vigencia.desc"
    })
    r.raise_for_status()
    rows = r.json()

    new_rows = []

    for row in rows:
        new_row = {
            "id": row["id"],

            # replace FK ids with names in the same positions
            "proveedor": (row.get("proveedores") or {}).get("nombre"),
            "ingrediente": (row.get("ingredientes") or {}).get("nombre"),
            "unidad": (row.get("unidad_de_medida") or {}).get("nombre"),

            "presentacion": row.get("presentacion"),
            "costo_presentacion": row.get("costo_presentacion"),
            "fecha_vigencia": row.get("fecha_vigencia"),
            "presentacion_raw": row.get("presentacion_raw"),
        }

        new_rows.append(new_row)

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
