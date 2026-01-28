from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uuid
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables FIRST before importing other modules
load_dotenv()

# Import after environment is loaded
from models import ChatRequest, ChatResponse, ConversationState, StudentData
from langgraph_workflow import LearningAssistantWorkflow

app = FastAPI(title="Learning Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fix mobile + deployment issues)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize workflow
workflow_manager = LearningAssistantWorkflow()

# In-memory session storage (in production, use Redis or database)
session_states = {}


def get_or_create_session(session_id: str):
    """Get or create a conversation state for a session"""
    if session_id not in session_states:
        session_states[session_id] = {
            "messages": [],
            "student_data": StudentData(),
            "current_step": "start",
            "session_id": session_id
        }
    return session_states[session_id]
    return session_states[session_id]


@app.get("/")
def read_root():
    return {"message": "Learning Assistant API", "status": "running"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint that processes student messages"""
    try:
        # Get or create session state
        session_state = get_or_create_session(request.session_id)
        
        # Add user message to state
        session_state["messages"].append({
            "role": "user",
            "content": request.message
        })
        
        # Prepare state for LangGraph
        from langgraph_workflow import State
        
        # Ensure student_data is a StudentData instance (not dict)
        student_data = session_state["student_data"]
        if isinstance(student_data, dict):
            student_data = StudentData(**student_data)
        elif not isinstance(student_data, StudentData):
            student_data = StudentData()
        
        graph_state: State = {
            "messages": session_state["messages"],
            "student_data": student_data,
            "current_step": session_state.get("current_step", "start"),
            "session_id": request.session_id
        }
        
        # Run workflow
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Invoke workflow (LangGraph supports both sync and async)
        import asyncio
        try:
            # Try async invoke first (preferred)
            if hasattr(workflow_manager.app, 'ainvoke'):
                result = await workflow_manager.app.ainvoke(graph_state, config)
            else:
                # Fallback to sync invoke in thread
                result = await asyncio.to_thread(workflow_manager.app.invoke, graph_state, config)
        except Exception as e:
            # Final fallback
            print(f"Error in workflow invoke: {e}")
            result = await asyncio.to_thread(workflow_manager.app.invoke, graph_state, config)
        
        # Update session state
        # Convert student_data back for storage
        student_data_result = result["student_data"]
        if isinstance(student_data_result, StudentData):
            student_data_storage = student_data_result
        elif isinstance(student_data_result, dict):
            student_data_storage = StudentData(**student_data_result)
        else:
            student_data_storage = StudentData()
        
        session_states[request.session_id] = {
            "messages": result["messages"],
            "student_data": student_data_storage,
            "current_step": result.get("current_step", "start"),
            "session_id": request.session_id
        }
        
        # Get last assistant message
        assistant_messages = [m for m in result["messages"] if m.get("role") == "assistant"]
        response_text = assistant_messages[-1]["content"] if assistant_messages else "I'm here to help! How can I assist you today?"
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id
        )
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in chat endpoint: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
