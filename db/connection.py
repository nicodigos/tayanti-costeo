import requests
from config.settings import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_SCHEMA

BASE = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Prefer": "return=representation",

}

def rest_get(table, params=None):
    print("REST_GET", table, params)
    print("HEADERS", HEADERS) 
    return requests.get(
        f"{BASE}/{table}",
        headers=HEADERS,
        params=params or {},
    )

def rest_post(table, json):
    print("REST_POST", table, HEADERS)
    print("HEADERS", HEADERS) 
    return requests.post(
        f"{BASE}/{table}",
        headers=HEADERS,
        json=json,
    )

def rest_patch(table, row_id, json):
    return requests.patch(
        f"{BASE}/{table}?id=eq.{row_id}",
        headers=HEADERS,
        json=json,
    )

def rest_delete(table, row_id):
    return requests.delete(
        f"{BASE}/{table}?id=eq.{row_id}",
        headers=HEADERS,
    )
