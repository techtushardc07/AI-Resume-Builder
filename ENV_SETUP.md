# Environment Variables Setup

Create a `.env` file in the `backend` directory with the following content:

```env
# OpenAI API Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# Supabase Configuration (REQUIRED)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Webhook URL (OPTIONAL - leave empty if not using webhooks)
# For testing, use https://webhook.site to get a free URL
# Or leave empty - the system works fine without it!
WEBHOOK_URL=
```

## How to create the `.env` file:

### Option 1: Using PowerShell
```powershell
cd backend
@"
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
WEBHOOK_URL=your_webhook_url_here
"@ | Out-File -FilePath .env -Encoding utf8
```

### Option 2: Using Notepad
1. Open Notepad
2. Copy and paste the content above (replace placeholder values)
3. Save as `.env` in the `backend` directory
4. Make sure to save as "All Files" type, not .txt

### Option 3: Using Command Line
```powershell
cd backend
echo OPENAI_API_KEY=your_openai_api_key_here > .env
echo SUPABASE_URL=https://your-project.supabase.co >> .env
echo SUPABASE_KEY=your_supabase_anon_key_here >> .env
echo WEBHOOK_URL=your_webhook_url_here >> .env
```

## Getting Your API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in `.env`

### Supabase Credentials
1. Go to https://supabase.com/
2. Create a project (or use existing)
3. Go to Settings > API
4. Copy:
   - Project URL → `SUPABASE_URL`
   - anon public key → `SUPABASE_KEY`

### Webhook URL (Optional)
- Use https://webhook.site/ for testing
- Or provide your own webhook endpoint
- Leave empty if you don't need webhooks

## Important Notes

- Never commit the `.env` file to git (it's already in .gitignore)
- Replace all placeholder values with your actual keys
- Restart the server after creating/updating `.env`
