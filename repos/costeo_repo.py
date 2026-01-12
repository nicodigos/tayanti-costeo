from db.connection import rest_get

TABLE = "vw_receta_costos"

def list_all():
    r = rest_get(TABLE, {
        "select": "receta_especifica_id,receta_nombre,version,costo_total,costo_unitario",
        "order": "receta_nombre,version"
    })
    r.raise_for_status()
    return r.json()
