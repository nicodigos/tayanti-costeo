from db.connection import rest_get

def fetch_lookup(table: str, id_col="id", label_col="nombre", order_by=None):
    params = {
        "select": f"{id_col},{label_col}",
        "order": order_by or label_col
    }
    r = rest_get(table, params)
    r.raise_for_status()
    data = r.json() or []
    return [(row[id_col], row[label_col]) for row in data]


def fetch_pip_lookup():
    """
    Ingredientes específicos: proveedor_ingrediente_precios
    Options: [(pip_id, "Proveedor | Ingrediente | presentacion unidad | fecha"), ...]
    """
    r = rest_get("proveedor_ingrediente_precios", {
        "select": (
            "id,presentacion,fecha_vigencia,"
            "proveedores(nombre),ingredientes(nombre),unidad_de_medida(nombre)"
        ),
        "order": "fecha_vigencia.desc"
    })
    r.raise_for_status()
    data = r.json() or []

    out = []
    for row in data:
        prov = (row.get("proveedores") or {}).get("nombre", "Proveedor?")
        ing  = (row.get("ingredientes") or {}).get("nombre", "Ingrediente?")
        uni  = (row.get("unidad_de_medida") or {}).get("nombre", "Unidad?")
        pres = row.get("presentacion")
        fv   = row.get("fecha_vigencia")
        label = f"{prov} | {ing} | {pres} {uni} | {fv}"
        out.append((row["id"], label))
    return out


def fetch_rie_lookup():
    """
    Recetas con versión: recetas_insumo_especifica
    Options: [(rie_id, "Receta | Version | cantidad unidad | chef"), ...]
    """
    r = rest_get("recetas_insumo_especifica", {
        "select": (
            "id,version,cantidad,"
            "recetas_insumo(nombre),unidad_de_medida(nombre),chef_responsable(nombre)"
        ),
        "order": "id.desc"
    })
    r.raise_for_status()
    data = r.json() or []

    out = []
    for row in data:
        rec  = (row.get("recetas_insumo") or {}).get("nombre", "Receta?")
        ver  = row.get("version", "")
        qty  = row.get("cantidad")
        uni  = (row.get("unidad_de_medida") or {}).get("nombre", "Unidad?")
        chef = (row.get("chef_responsable") or {}).get("nombre", "Chef?")
        label = f"{rec} | {ver} | {qty} {uni} | {chef}"
        out.append((row["id"], label))
    return out
