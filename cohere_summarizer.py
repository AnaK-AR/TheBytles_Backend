import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def summarize_user(bio: str, capability: str, cv_text: str, skill_names:str) -> str:
    try:
        prompt = f"""
        Candidate summary:
        
        SKILLS: 
        {skill_names}
        
        
        CV TEXT: 
        {cv_text}
        
        BIO: 
        {bio}
        
        CAPABILITY: 
        {capability}
        
        Reformat the above into exactly **one single line** with these **three** fields, separated by middle-dots (` · `), no real newlines or blank lines, and no bullets.

        Follow the follow template:
        Responsibilities: [key responsibilities in jobs and projects. Describe in present tense] · Skills: [comma-separated list of each and every single skill that shows up; do not dedupe, even if repeated. Include all skills, do not say anything along the lines of: "...and more.", "...among outhers"]

        Output exactly that one line—nothing else.
        """

         # Generacion del texto con Cohere
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.0
        )

        # Limpieza y separacion de lineas validas
        summary = response.generations[0].text.strip()
        
        return summary

    except Exception as e:
        print(f"Cohere summary generation error: {e}")
        return "[Error generating summary with Cohere]"