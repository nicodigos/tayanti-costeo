from db.connection import rest_get

def supabase_healthcheck():
    try:
        r = rest_get("tipo_de_insumo", {"limit": 1})
        if r.status_code == 200:
            return True, "Connected to Supabase via REST"
        return False, f"Supabase REST error {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)
