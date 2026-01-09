import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA", "public").strip()


def validate_settings() -> tuple[bool, str]:
    if not SUPABASE_URL:
        return False, "Missing SUPABASE_URL in .env"
    if not SUPABASE_SERVICE_ROLE_KEY:
        return False, "Missing SUPABASE_SERVICE_ROLE_KEY in .env"
    return True, "Settings OK"
