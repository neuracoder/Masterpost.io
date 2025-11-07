from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    return supabase
