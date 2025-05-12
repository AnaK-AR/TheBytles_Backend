import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def extract_roles(rfp_text: str) -> list:
    try:
        prompt = f"""
You are an AI assistant analyzing an RFP (Request for Proposal). Your task is to extract several distinct paragraphs, each describing **one specific role** required by the project.

Each paragraph must:
- Begin with the role name in bold (e.g., **Frontend Developer**, **QA Engineer**) embedded naturally in the **first sentence**.
- Be written as a single, clear paragraph in **plain text**, with no bullet points or line breaks.
- Include detailed, **specific tasks**, **responsibilities**, **required skills**, and **preferred experience**.
- Avoid vague phrases like "good communication" unless directly tied to specific job duties.
- Cover as many distinct roles as needed to represent all major responsibilities in the RFP — do **not merge unrelated duties into one role**.

Only output a sequence of role-labeled paragraphs as described above — no lists, titles, summaries, or explanations outside of the paragraphs themselves.

RFP TEXT:
{rfp_text}
"""

        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=800,
            temperature=0.3
        )

        result = response.generations[0].text.strip()
        roles = [p.strip() for p in result.split('\n') if p.strip()]
        return roles

    except Exception as e:
        print(f"Cohere role generation error: {e}")
        return ["[Error extracting roles from RFP]"]