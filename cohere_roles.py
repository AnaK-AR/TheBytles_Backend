import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def extract_roles(rfp_text: str) -> list:
    try:
        '''
                prompt = f"""
You are an AI assistant analyzing an RFP (Request for Proposal). Your task is to write multiple paragraphs, each describing a **distinct and clearly named role** required by the project.

Each paragraph must:
- Begin with the **role name*, written directly into the **first sentence** (e.g., "The **Project Manager** will be responsible for...").
- Be written as a **single continuous paragraph** — absolutely **no line breaks**, bullet points, markdown formatting outside of the role name, or separate titles before the paragraph.
- Describe specific **tasks**, **responsibilities**, **required skills**, and **preferred experience** related to that role.
- Never generalize or combine responsibilities across unrelated roles — instead, write more roles to cover the full scope.
- Avoid headings, summaries, lists, or transitions outside of the paragraph content itself.

Do not add any spacing or formatting between paragraphs beyond a single space. The output must be plain text with all role names naturally embedded into their own single paragraph.

RFP TEXT:
{rfp_text}
"""
        '''
        prompt = f"""
        RFP (Request for Proposal) TEXT:
        {rfp_text}
        
        You’ll extract **one role per paragraph**. For each role, output **one single line** using middle-dots (` · `) to separate fields—no real newlines inside the line, no extra commentary, no bullets. Paragraphs (i.e. different roles) should be separated by a single real blank line.
        Make as many roles as necessary to meet **ALL** the RFP's needs, as long as theyre in these Accenture career areas:
Artificial intelligence & data science; Cloud; Consulting; Creative & design; Customer & user experience; Emerging technology; Engineering & manufacturing; Industries; Marketing & communications; Operations & delivery; Product development; Programming languages; Program & project management; Research & innovation; Sales & account management; Security; Software engineering; Strategy; Technology; Technology platforms; Internal functions.

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