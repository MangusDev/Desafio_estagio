
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("https://hjjavtuvbdlqmuqwzsib.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_MWCRGcrVvcyHZKicQgGeyg_rEdCcKHr")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_interacao(tema, usuario_id=None):
    data = {
        "tema": tema,
        "usuario_id": usuario_id
    }
    supabase.table("interacoes").insert(data).execute()

def listar_interacoes():
    response = supabase.table("interacoes").select("*").order("timestamp", desc=True).limit(10).execute()
    return response.data