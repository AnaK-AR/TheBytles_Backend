import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client
from cohere_keypoints import keypoint_generation

load_dotenv()

# Supabase setup
supabase = create_client(os.getenv("VITE_SUPABASE_URL"), os.getenv("VITE_SUPABASE_ANON_KEY"))

def generate_keypoints(user_id):
    try:
        print(f"\nStarting key points for {user_id}")

        user = supabase.table("User").select("*").eq("userId", user_id).single().execute().data
        if not user or not user.get("ai_summary"):
            print("Missing user or ai_summary")
            return False

        actual_skills = user.get("ai_summary")
        goal_data = supabase.table("Goal").select("description").eq("goalUserId", user_id).execute().data
        user_goals = ". ".join([goal["description"] for goal in goal_data if goal.get("description")])
        

        keypoints = keypoint_generation(actual_skills, user_goals)
        
        if isinstance(keypoints, str):
            keypoints = keypoints.strip().splitlines()
    
        for keypoint in keypoints:
            print("Inserting keypoint:", keypoint)

            supabase.table("Grow").insert({
                "user_grow_id": user_id,
                "Recomendation": keypoint,
                "Generated": datetime.now().isoformat(),
            }).execute()

        print("Keypoints saved for user")
        return True

    except Exception as e:
        print(f"Error generating keypoints for user {user_id}: {e}")
        return False
