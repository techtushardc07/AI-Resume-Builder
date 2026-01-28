# Backend - Learning Assistant API

FastAPI backend with LangGraph workflow for the Learning Assistant system.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
WEBHOOK_URL=your_webhook_url_here
```

3. **Set up Supabase:**
   - Go to your Supabase project
   - Navigate to SQL Editor
   - Run the SQL from `supabase_setup.sql`

4. **Run the server:**
```bash
python main.py
# Or:
uvicorn main:app --reload --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

- **main.py**: FastAPI application and endpoints
- **langgraph_workflow.py**: LangGraph workflow with nodes for routing and data collection
- **models.py**: Pydantic models for type validation
- **supabase_client.py**: Supabase integration for data persistence
