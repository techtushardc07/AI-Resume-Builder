from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum


class Track(str, Enum):
    ACADEMIC = "academic"
    SKILL = "skill"
    WELLBEING = "wellbeing"


class StudentData(BaseModel):
    student_name: Optional[str] = None
    student_age: Optional[int] = None
    learning_goal: Optional[str] = None
    track: Optional[Track] = None


class ConversationState(BaseModel):
    messages: list[dict] = []
    student_data: StudentData = StudentData()
    current_step: str = "start"


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


class WebhookPayload(BaseModel):
    student_name: str
    student_age: int
    learning_goal: str
    track: str
