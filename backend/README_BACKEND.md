# Backend Setup Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** database installed and running
3. **Gemini API Key** (free from Google)

## Step 1: Get Gemini API Key (FREE)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

## Step 2: Install PostgreSQL

### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember your password!

### Mac:
```bash
brew install postgresql
brew services start postgresql
```

### Linux:
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

## Step 3: Create Database

Open PostgreSQL command line (psql) and run:

```sql
CREATE DATABASE wiki_quiz_db;
```

Or use pgAdmin GUI tool.

## Step 4: Setup Backend

1. **Navigate to backend folder:**
```bash
cd wiki-quiz-app/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

Edit the `.env` file with your actual values:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/wiki_quiz_db
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Replace:
- `YOUR_PASSWORD` with your PostgreSQL password
- `your_actual_gemini_api_key_here` with your Gemini API key

## Step 6: Run the Backend

```bash
python -m uvicorn app.main:app --reload
```

You should see:
```
Starting Wiki Quiz Generator API...
Database tables created successfully!
Server running on http://0.0.0.0:8000
```

## Step 7: Test the API

Open browser and go to:
- **API Docs:** http://localhost:8000/docs
- **Root:** http://localhost:8000/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/quiz/generate` | Generate new quiz |
| GET | `/api/quiz/{id}` | Get specific quiz |
| GET | `/api/quiz/list` | Get all quizzes |

## Testing with cURL

Generate a quiz:
```bash
curl -X POST "http://localhost:8000/api/quiz/generate" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'
```

## Common Issues

### Issue: Database connection failed
**Solution:** Check PostgreSQL is running and credentials in `.env` are correct

### Issue: Gemini API error
**Solution:** Verify your API key is correct in `.env` file

### Issue: Module not found
**Solution:** Make sure virtual environment is activated and requirements are installed

## File Structure

```
backend/
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI app & endpoints
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # Database models
│   ├── schemas.py           # API schemas
│   ├── scraper.py           # Wikipedia scraper
│   └── quiz_generator.py   # LLM quiz generation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README_BACKEND.md       # This file
```

## Next Steps

After backend is running, proceed to frontend setup!