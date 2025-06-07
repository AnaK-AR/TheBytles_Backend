import os
import requests
import io
import fitz  # PyMuPDF
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client
from transformers import AutoTokenizer
from cohere_summarizer import summarize_user
from cohere_embed import generate_embedding


load_dotenv()

supabase = create_client(os.getenv("VITE_SUPABASE_URL"), os.getenv("VITE_SUPABASE_ANON_KEY"))

# Tokenizador para truncar texto por token
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

def trim_to_token_limit(text, max_tokens=1024):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens)

# Descargar PDF pra extraccion de texto
def download_and_extract_text(cv_url):
    response = requests.get(cv_url)
    response.raise_for_status()
    with io.BytesIO(response.content) as pdf_file:
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
    return text

# Generar resumen del usuario con IA y embedding
def generate_user_summary(user_id):
    try:
        print(f"\nStarting summary for {user_id}")

        # Informacion del usuario
        user = supabase.table("User").select("*").eq("userId", user_id).single().execute().data
        if not user or not user.get("cv_url"):
            print("Missing user or cv_url")
            return False

        # Recorte del texto del CV
        pdf_text = download_and_extract_text(user["cv_url"])
        trimmed_cv = trim_to_token_limit(pdf_text)
         
        # Informacion adicional del perfil
        bio = user.get("bio", "")
        capability = user.get("capability", "")
       
       # Listas de habilidades del usuario
        user_skills = supabase.table("User_Skills").select("*, Skills(SkillName)").eq('userid', user_id).execute().data
        skill_names = [row["Skills"]["SkillName"] for row in user_skills]
        
        # Generacion del resumen, llamando a Cohere
        summary = summarize_user(bio, capability, trimmed_cv, skill_names)
        print("AI Summary:\n", summary)
        embedding = generate_embedding(summary, input_type="search_query")
        
        # Guardar resumen y embedding en Supabase
        supabase.table("User").update({
            "ai_summary": summary,
            "summary_generated_at": datetime.utcnow().isoformat(),
            "embedding": embedding,
        }).eq("userId", user_id).execute()

        print("Summary saved for user")
        return True

    except Exception as e:
        print(f"Error generating summary for user {user_id}: {e}")
        return False
