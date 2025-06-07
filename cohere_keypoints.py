import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def keypoint_generation(actual_skills: str, user_goals: str) -> list:
    try:
        prompt = f"""
The user with the following skills:
{actual_skills}

Aspires to reach the following goals:
{user_goals}

You are an expert career coach. Based on the user's skills and goals, generate four personalized micro-growth tasks. 
Half must be focused on soft skills, and half must be focused on technical skills, where each item must:
– Be a standalone sentence under 25 words.
– Read like a habit or project someone can begin immediately.
– Be actionable and task-based.
– Avoid generic advice (such as “build your brand” or “expand your network.”).
- ****Avoid at all costs introductions, conclusions, or transitions.****
– Be formatted as a plain list of sentences (no bullets, no numbering, no headings).
– The output must consist of **exactly four separate lines**, each with one task, and nothing else.
    """
        # Generacion del texto con Cohere
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.3
        )

        # Limpieza y separacion de lineas validas
        keypoints = [kp.strip() for kp in response.generations[0].text.strip().splitlines() if kp.strip()]
        
        return keypoints
    
    except Exception as e:
        print(f"Cohere keypoints generation error: {e}")
        return ["[Error generating keypoints for user.]"]