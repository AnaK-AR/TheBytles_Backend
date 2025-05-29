import os
from supabase import create_client, Client
import cohere
from time import sleep
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_embedding(text: str, input_type: str = "search_document") -> list:
    try:
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type=input_type
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"Embedding generation error: {e}")
        return []

def fetch_missing_embeddings():
    response = supabase.table("Cert_Recomendation") \
        .select("id_recomendation, Cert_Des") \
        .is_("cert_embedding", "null") \
        .execute()
    
    return response.data if response.data else []

def update_embedding(id_recomendation: str, embedding: list[float]):
    response = supabase.table("Cert_Recomendations") \
        .update({"cert_embedding": embedding}) \
        .eq("id_recomendation", id_recomendation) \
        .execute()
    
    return response

# ---  LOOP ---
certs = fetch_missing_embeddings()

print(f"Found {len(certs)} certs missing embeddings.")

for i, certif in enumerate(certs):
    print(f"[{i+1}/{len(certs)}] Processing cert ID: {certif['id_recomendation']}")
    
    description = certif["Cert_Des"]
    embedding = generate_embedding(description)

    if embedding:
        update_embedding(certif["id_recomendation"], embedding)
        print("Updated successfully.")
    else:
        print("Skipped due to error.")
    
    sleep(1.2)