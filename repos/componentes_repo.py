from db.connection import rest_get, rest_post, rest_patch, rest_delete
TABLE = "componentes"

def list_all():
    r = rest_get(TABLE, {"order": "nombre"})
    r.raise_for_status()
    return r.json()

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
