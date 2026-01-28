from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from models import Track, StudentData
from supabase_client import SupabaseManager

import httpx
import os
import re
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()


# -------------------------
# STATE DEFINITION
# -------------------------
class State(TypedDict):
    messages: Annotated[list, "messages"]
    student_data: StudentData
    current_step: str
    session_id: str


# -------------------------
# WORKFLOW CLASS
# -------------------------
class LearningAssistantWorkflow:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
        self.supabase = SupabaseManager()
        self.webhook_url = os.getenv("WEBHOOK_URL", "")

        self.graph = self._build_graph()
        self.app = self.graph.compile(checkpointer=MemorySaver())

    # -------------------------
    # ROUTER
    # -------------------------
    def _classify_track(self, message: str) -> Track:
        msg = message.lower()

        skill_keywords = ["career", "coding", "programming", "skill", "tools", "communication"]
        wellbeing_keywords = ["stress", "focus", "motivation", "anxiety", "worry", "struggle", "mental", "burnout"]

        if any(k in msg for k in skill_keywords):
            return Track.SKILL
        if any(k in msg for k in wellbeing_keywords):
            return Track.WELLBEING

        return Track.ACADEMIC

    # -------------------------
    # INFO EXTRACTION
    # -------------------------
    def _extract_info(self, message: str, field: str, student_data: StudentData):
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
Extract {field} from the user's message.

Current data:
Name: {student_data.student_name or "None"}
Age: {student_data.student_age or "None"}
Goal: {student_data.learning_goal or "None"}

If not present, return only: NOT_FOUND
"""),
            ("user", message)
        ])

        chain = prompt | self.llm
        result = chain.invoke({}).content.strip()

        if not result or result.upper() == "NOT_FOUND":
            return None

        if field == "student_age":
            nums = re.findall(r"\d+", result)
            if nums:
                age = int(nums[0])
                if 5 <= age <= 100:
                    return age
            return None

        return result

    # -------------------------
    # MISSING FIELD
    # -------------------------
    def _get_missing_field(self, data: StudentData):
        if not data.student_name:
            return "student_name"
        if not data.student_age:
            return "student_age"
        if not data.learning_goal:
            return "learning_goal"
        return None

    # -------------------------
    # WEBHOOK
    # -------------------------
    def _trigger_webhook(self, data: StudentData):
        if not self.webhook_url:
            print("⚠ WEBHOOK_URL not set")
            return

        payload = {
            "student_name": data.student_name,
            "student_age": data.student_age,
            "learning_goal": data.learning_goal,
            "track": data.track.value
        }

        try:
            httpx.post(self.webhook_url, json=payload, timeout=10)
            print("✅ Webhook sent")
        except Exception as e:
            print("❌ Webhook error:", e)

    # -------------------------
    # NODES
    # -------------------------
    def start_node(self, state: State):
        last_msg = state["messages"][-1]["content"]
        state["student_data"].track = self._classify_track(last_msg)
        state["current_step"] = "router"
        return state

    def router_node(self, state: State):
        track = state["student_data"].track

        if track == Track.ACADEMIC:
            state["current_step"] = "academic"
        elif track == Track.SKILL:
            state["current_step"] = "skill"
        else:
            state["current_step"] = "wellbeing"

        return state

    def academic_track_node(self, state: State):
        return self._process_track(state, Track.ACADEMIC)

    def skill_track_node(self, state: State):
        return self._process_track(state, Track.SKILL)

    def wellbeing_track_node(self, state: State):
        return self._process_track(state, Track.WELLBEING)

    # -------------------------
    # CORE LOGIC
    # -------------------------
    def _process_track(self, state: State, track: Track):
        msg = state["messages"][-1]["content"]
        data = state["student_data"]
        data.track = track

        missing = self._get_missing_field(data)

        if missing:
            extracted = self._extract_info(msg, missing, data)

            if extracted:
                if missing == "student_name":
                    data.student_name = extracted
                elif missing == "student_age":
                    data.student_age = extracted
                elif missing == "learning_goal":
                    data.learning_goal = extracted

            missing = self._get_missing_field(data)

        if missing:
            questions = {
                "student_name": "May I know your name?",
                "student_age": "Could you tell me your age?",
                "learning_goal": "What would you like help with?"
            }
            response = questions[missing]

        else:
            self.supabase.save_student_data(state["session_id"], data)
            self._trigger_webhook(data)

            response = (
                f"Thank you {data.student_name}. "
                f"I’ve recorded your details and routed you to the {data.track.value.replace('_',' ').title()} track. "
                f"Our team will help you with: {data.learning_goal}"
            )

        state["messages"].append({"role": "assistant", "content": response})
        return state

    # -------------------------
    # BUILD GRAPH
    # -------------------------
    def _build_graph(self):
        g = StateGraph(State)

        g.add_node("start", self.start_node)
        g.add_node("router", self.router_node)
        g.add_node("academic", self.academic_track_node)
        g.add_node("skill", self.skill_track_node)
        g.add_node("wellbeing", self.wellbeing_track_node)

        g.set_entry_point("start")
        g.add_edge("start", "router")

        def route(state: State):
            return state["current_step"]

        g.add_conditional_edges("router", route)
        g.add_edge("academic", END)
        g.add_edge("skill", END)
        g.add_edge("wellbeing", END)

        return g
