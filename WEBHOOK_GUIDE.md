# Webhook URL Guide

## What is a Webhook?

A webhook is like a callback URL - when your system collects all student information (name, age, learning goal), it automatically sends a POST request to your webhook URL with the data. This allows you to:
- Send notifications (email, SMS)
- Integrate with other services (CRM, databases)
- Trigger automated workflows
- Log data to external systems

## Do You Need a Webhook?

**No!** The webhook is completely optional. Your system will work perfectly without it. All student data is still saved to Supabase database.

## Options for Webhook URL

### Option 1: Leave It Empty (Simplest) ⭐ Recommended for Testing

In your `.env` file, simply leave it empty:
```env
WEBHOOK_URL=
```

Or don't include it at all. The system will work fine and just print a warning message.

### Option 2: Use Webhook.site (Free Testing Tool)

This is perfect for testing and seeing what data is sent:

1. **Go to https://webhook.site**
2. **Copy your unique URL** (it looks like: `https://webhook.site/unique-id-here`)
3. **Paste it in your `.env` file:**
   ```env
   WEBHOOK_URL=https://webhook.site/your-unique-id-here
   ```
4. **Test it!** When student data is collected, visit webhook.site to see the POST request with all the data

**Example webhook payload you'll receive:**
```json
{
  "student_name": "John Doe",
  "student_age": 16,
  "learning_goal": "I need help with algebra",
  "track": "academic"
}
```

### Option 3: Create Your Own Simple Webhook Endpoint

If you want to handle the data yourself, here are some options:

#### A. Using a Free Service (Recommended)

**Zapier Webhooks:**
1. Go to https://zapier.com
2. Create a free account
3. Create a new Zap
4. Choose "Webhooks by Zapier" → "Catch Hook"
5. Copy the webhook URL they give you
6. Use it in your `.env` file

**Make.com (formerly Integromat):**
1. Go to https://make.com
2. Create a free account
3. Create a scenario with "Webhooks" → "Custom webhook"
4. Copy the webhook URL

#### B. Create Your Own Server (Advanced)

If you want to build your own webhook endpoint, here's a simple FastAPI example:

**Create a file `webhook_server.py`:**
```python
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class StudentData(BaseModel):
    student_name: str
    student_age: int
    learning_goal: str
    track: str

@app.post("/webhook")
async def receive_webhook(data: StudentData):
    print(f"Received student data: {data}")
    
    # Do something with the data:
    # - Send email notification
    # - Save to another database
    # - Trigger an action
    
    return {"status": "received", "data": data}
```

Run it:
```bash
uvicorn webhook_server:app --port 8001
```

Then use: `WEBHOOK_URL=http://localhost:8001/webhook`

### Option 4: Use ngrok to Expose Local Server (Testing)

If you have a local server and want to test it:

1. **Install ngrok:** https://ngrok.com/download
2. **Start your webhook server** (like the example above)
3. **Run ngrok:**
   ```bash
   ngrok http 8001
   ```
4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
5. **Use it in `.env`:** `WEBHOOK_URL=https://abc123.ngrok.io/webhook`

## Current Code Behavior

Looking at `langgraph_workflow.py`, the webhook code is:
```python
if not self.webhook_url:
    print("⚠ WEBHOOK_URL not set")
    return  # Just skips webhook, continues normally
```

So if you don't set it, the system:
- ✅ Still works perfectly
- ✅ Still saves data to Supabase
- ✅ Still processes all student information
- ⚠️ Just prints a warning (you can ignore it)

## Recommendation

**For now:** Leave `WEBHOOK_URL` empty or use **webhook.site** to see what data would be sent.

**Later:** If you need to integrate with other services, use Zapier, Make.com, or create your own endpoint.

## Quick Setup

**No webhook (works fine):**
```env
WEBHOOK_URL=
```

**With webhook.site (see the data):**
```env
WEBHOOK_URL=https://webhook.site/your-unique-id
```

That's it! Your system will work either way. 🎉
