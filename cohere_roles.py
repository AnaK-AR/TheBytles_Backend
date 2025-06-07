import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def extract_roles(rfp_text: str) -> list:
    try:
        prompt = f"""
        RFP (Request for Proposal) TEXT:
        {rfp_text}
        
        You’ll extract **one role per paragraph**. For each role, output **one single line** using middle-dots (` · `) to separate fields—no real newlines inside the line, no extra commentary, no bullets. Paragraphs (i.e. different roles) should be separated by a single real blank line.
        Make as many roles as necessary to meet **ALL** the RFP's needs, as long as theyre in these Accenture career areas:
Artificial intelligence & data science; Cloud; Consulting; Creative & design; Customer & user experience; Emerging technology; Engineering & manufacturing; Industries; Marketing & communications; Operations & delivery; Product development; Programming languages; Program & project management; Research & innovation; Sales & account management; Security; Software engineering; Strategy; Technology; Technology platforms; Internal functions.
        Do not mention the company name at any point.

        Use exactly this template for each line:
        Role: [Role title; one-sentence overview] · Responsibilities: [key duties for that role] · Skills: [comma-separated list of all required skills]

        Output multiple paragraphs (one per role), each containing exactly one line in the format above. Nothing else.
        """


        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.3
        )

        result = response.generations[0].text.strip()
        roles = [p.strip() for p in result.split('\n') if p.strip()]
        return roles

    except Exception as e:
        print(f"Cohere role generation error: {e}")
        return ["[Error extracting roles from RFP]"]