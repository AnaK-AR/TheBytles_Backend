import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def summarize_user(bio: str, capability: str, cv_text: str, skill_weighted:str) -> str:
    try:
        '''
        prompt = f"""
You are an AI assistant summarizing a candidate’s professional profile. Your task is to write a **single, self-contained paragraph** that clearly describes the candidate’s technical skills, relevant experience, and professional strengths.

Do not include:
- The candidate’s name or any personal identifiers
- Any introductions like “Here is a summary of the candidate’s profile”
- Any conclusions like “This highlights their skills” or “This overview is useful for...”
- Any bullet points, headings, or lists

Only output a clean, concise paragraph focused **exclusively** on the candidate's **skills**, **technologies used**, **project experience**, and **professional capabilities** — optimized for semantic embedding and role matching.

BIO:
{bio}

CAPABILITY:
{capability}

CV TEXT:
{cv_text}

SKILLS:
{skill_names}
"""
'''
        prompt = f"""
        Candidate summary:
        
        SKILLS: 
        {skill_weighted}
        
        CV TEXT: 
        {cv_text}
        
        BIO: 
        {bio}
        
        CAPABILITY: 
        {capability}
        
        Reformat the above into exactly this three‐line template, with:
        1. No blank lines between sections.
        2. No bullet points.
        3. Projects listed as individual sentences separated by semicolons.

        Template:
        About: [one paragraph summarizing the candidate] · Skills: [comma-separated list of skills. include absolutely all of them that are mentioned.] · Projects: [Description of proyect1; Description of proyect2; Description of proyect3...]

        Output only those three fields in the same line, nothing else.
        """

        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.0
        )

        summary = response.generations[0].text.strip()
        return summary

    except Exception as e:
        print(f"Cohere summary generation error: {e}")
        return "[Error generating summary with Cohere]"