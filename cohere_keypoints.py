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
        
Based on the following background and skills, provide a clear and specific list of task-based, habit-forming recommendations to accelerate the user’s professional growth. 
Each item should be a complete sentence focused on a specific action, project, or habit that supports career advancement. Do not use bullet points or numbers. 
Return the output as a list of sentences, without any introductory or summary text.
        """

        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.3
        )

        result = response.generations[0].text.strip()
        keypoints = [p.strip() for p in result.split('\n') if p.strip()]
        return keypoints

    except Exception as e:
        print(f"Cohere keypoibts generation error: {e}")
        return ["[Error generating keypoints for user.]"]