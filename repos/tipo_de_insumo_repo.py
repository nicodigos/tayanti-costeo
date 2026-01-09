from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "tipo_de_insumo"

def list_all():
    r = rest_get(TABLE, {"order": "nombre"})
    r.raise_for_status()
    return r.json()

def create(nombre, merma):
    r = rest_post(TABLE, {"nombre": nombre, "merma": float(merma)})
    r.raise_for_status()
    return r.json()

def update(row_id, nombre, merma):
    r = rest_patch(TABLE, row_id, {"nombre": nombre, "merma": float(merma)})
    r.raise_for_status()
    return r.json()

def delete(row_id):
    r = rest_delete(TABLE, row_id)
    r.raise_for_status()
