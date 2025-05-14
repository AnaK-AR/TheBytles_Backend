import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

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