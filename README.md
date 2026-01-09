# Streamlit CRUD (Supabase REST)

This app uses Supabase PostgREST via `supabase-py` (HTTPS) for CRUD, avoiding direct Postgres port 5432.

## Setup (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy .env.example -> .env and fill values.

## Run
streamlit run app.py
