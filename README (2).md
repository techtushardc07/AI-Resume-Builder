# AI-Powered Personalized Learning Assistant

A smart digital school receptionist + tutor intake system supporting **SDG 4 – Quality Education**. The system understands student queries, classifies learning needs, collects required learner information, and sends structured data to a webhook.

## Features

- **Natural Language Processing**: Accepts and understands student queries in natural language
- **Intelligent Routing**: Classifies students into three tracks:
  - **Academic Support**: Exam, subjects, homework, concepts
  - **Skill Development**: Career, coding, communication, tools
  - **Mental & Learning Wellbeing**: Stress, focus, motivation, learning difficulties
- **Data Collection**: Systematically collects student name, age, and learning goal
- **Supabase Integration**: Stores student sessions in Postgres database
- **Webhook Integration**: Triggers webhook when all required data is collected
- **Conversational UI**: Clean chat-style interface built with React

## Tech Stack

- **Frontend**: React 18 + Vite
- **Backend**: Python FastAPI
- **AI/Workflow**: LangGraph + LangChain + OpenAI
- **Database**: Supabase (PostgreSQL)

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── langgraph_workflow.py   # LangGraph workflow definition
│   ├── models.py               # Pydantic models
│   ├── supabase_client.py      # Supabase integration
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Styles
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account (free tier works)
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory:
```bash
cp .env.example .env
```

5. Edit `.env` and add your credentials:
```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
WEBHOOK_URL=your_webhook_url_here
```

6. Set up Supabase table:

Create a table in your Supabase project with the following SQL:

```sql
CREATE TABLE student_sessions (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT UNIQUE NOT NULL,
  student_name TEXT,
  student_age INTEGER,
  learning_goal TEXT,
  track TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_session_id ON student_sessions(session_id);
```

7. Run the backend server:
```bash
python main.py
# Or using uvicorn directly:
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### POST /chat

Send a chat message and receive an AI response.

**Request:**
```json
{
  "message": "I'm struggling with math homework",
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "response": "I'd be happy to help you with math homework! Could you please tell me your name?",
  "session_id": "unique-session-id"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Webhook Payload

When all student data is collected (name, age, learning goal), the system triggers a webhook with the following payload:

```json
{
  "student_name": "John Doe",
  "student_age": 16,
  "learning_goal": "I need help with algebra",
  "track": "academic"
}
```

The `track` field can be one of:
- `"academic"`
- `"skill"`
- `"wellbeing"`

## How It Works

1. **User sends a message** through the chat interface
2. **LangGraph workflow processes** the message:
   - `start_node`: Receives input and classifies the track
   - `router_node`: Routes to appropriate track node
   - Track nodes (`academic_track`, `skill_track`, `wellbeing_track`): Collect student information
3. **Information extraction**: Uses LLM to extract name, age, and learning goal from conversations
4. **Data collection**: Asks one clarification question at a time if information is missing
5. **Storage**: Saves data to Supabase when collected
6. **Webhook trigger**: Sends POST request to webhook URL when all data is complete

## Development Notes

- Session state is stored in-memory (use Redis in production)
- LangGraph checkpointer uses memory (use PostgreSQL checkpointer in production)
- The system asks one question at a time to avoid overwhelming students
- All tracks follow the same data collection flow but with different context

## GitHub Upload

To upload this project to GitHub:

1. **Install Git** (if not already installed)
2. **Run the automated setup script:**
   ```powershell
   .\setup_git.ps1
   ```
3. **Or follow the manual steps in `GIT_SETUP.md`**

## License

MIT
