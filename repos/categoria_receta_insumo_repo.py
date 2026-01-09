from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "categoria_receta_insumo"

def list_all():
    r = rest_get(TABLE, {"order": "nombre"})
    r.raise_for_status()
    return r.json()

def create(nombre):
    r = rest_post(TABLE, {"nombre": nombre})
    r.raise_for_status()
    return r.json()

def update(row_id, nombre):
    r = rest_patch(TABLE, row_id, {"nombre": nombre})
    r.raise_for_status()
    return r.json()

def delete(row_id):
    r = rest_delete(TABLE, row_id)
    r.raise_for_status()
