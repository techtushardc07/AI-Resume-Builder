import os
from supabase import create_client, Client
from typing import Dict, Optional
from models import StudentData, Track


class SupabaseManager:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        self.table_name = "student_sessions"
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the student_sessions table exists with required columns"""
        # Note: In production, you should create the table via Supabase dashboard or migrations
        # This is a placeholder to document the expected schema
        pass
    
    def save_student_data(self, session_id: str, student_data: StudentData) -> Dict:
        """Save student data to Supabase"""
        data = {
            "session_id": session_id,
            "student_name": student_data.student_name,
            "student_age": student_data.student_age,
            "learning_goal": student_data.learning_goal,
            "track": student_data.track.value if student_data.track else None,
            "created_at": "now()"
        }
        
        # Insert or update based on session_id
        result = self.client.table(self.table_name).upsert(
            data,
            on_conflict="session_id"
        ).execute()
        
        return result.data[0] if result.data else {}
    
    def get_student_data(self, session_id: str) -> Optional[StudentData]:
        """Retrieve student data from Supabase"""
        result = self.client.table(self.table_name).select("*").eq(
            "session_id", session_id
        ).execute()
        
        if result.data:
            row = result.data[0]
            return StudentData(
                student_name=row.get("student_name"),
                student_age=row.get("student_age"),
                learning_goal=row.get("learning_goal"),
                track=Track(row.get("track")) if row.get("track") else None
            )
        return None
