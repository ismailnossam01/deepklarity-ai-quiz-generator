# 🧠 AI Wiki Quiz Generator

**Transform any Wikipedia article into an interactive AI-powered quiz!**

Built with React, FastAPI, PostgreSQL, and Google Gemini AI as part of the DeepKlarity Technologies assignment.

---

## 🌐 Live Demo

- **Frontend (Vercel)**: https://deepklarity-ai-quiz-generator.vercel.app/
- **Backend API (Render)**: https://wiki-quiz-backend-qxjm.onrender.com/
- **API Documentation**: https://wiki-quiz-backend-qxjm.onrender.com/docs

> **Note**: Backend is hosted on Render free tier. First request after inactivity may take 30-60 seconds (cold start). Subsequent requests are instant.

---

## ✨ Features

### Core Features
- ✅ **AI-Powered Quiz Generation** - Generates 5-10 questions from any Wikipedia article
- ✅ **Intelligent Scraping** - Extracts key information using BeautifulSoup
- ✅ **Smart Caching** - Prevents duplicate scraping of same URLs
- ✅ **Quiz History** - View all previously generated quizzes
- ✅ **Interactive Quiz Mode** - Take quizzes with instant feedback
- ✅ **Related Topics** - Get suggestions for further reading

### Technical Features
- 📊 **Entity Extraction** - Identifies people, organizations, and locations
- 🎯 **Difficulty Levels** - Questions categorized as easy, medium, or hard
- 💾 **PostgreSQL Database** - Stores all quiz data persistently
- 🔄 **RESTful API** - Clean, well-documented endpoints
- 🎨 **Responsive UI** - Works on desktop, tablet, and mobile

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI/LLM**: Google Gemini 2.5 Flash
- **Scraping**: BeautifulSoup4
- **ORM**: SQLAlchemy

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: React Hooks

### DevOps
- **Backend Hosting**: Render
- **Frontend Hosting**: Vercel
- **Database**: Render PostgreSQL
- **Version Control**: Git/GitHub

---

## 📁 Project Structure

```
wiki-quiz-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app & endpoints
│   │   ├── database.py          # Database connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── scraper.py           # Wikipedia scraper
│   │   ├── quiz_generator.py   # Gemini AI integration
│   │   └── config.py            # Configuration
│   ├── requirements.txt
│   ├── .env
│   ├── Procfile
│   └── README_BACKEND.md
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── api.js               # API service
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── .env
│   └── README_FRONTEND.md
├── sample_data/
│   ├── test_urls.txt
│   ├── sample_response_1.json
│   └── sample_response_2.json
├── prompts.md                   # LLM prompt templates
├── SETUP_GUIDE.md              # Detailed setup instructions
└── README.md                    # This file
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

```bash
# 1. Clone repository
git clone 
cd wiki-quiz-app/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create PostgreSQL database
createdb wiki_quiz_db

# 5. Configure environment variables
cp .env.example .env
# Edit .env and add:
#   - DATABASE_URL
#   - GEMINI_API_KEY (get free from: https://makersuite.google.com/app/apikey)

# 6. Run server
python -m uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env: VITE_API_URL=http://localhost:8000

# 4. Run development server
npm run dev
```

Frontend will run on: http://localhost:5173

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| POST | `/api/quiz/generate` | Generate quiz from Wikipedia URL |
| GET | `/api/quiz/{id}` | Get specific quiz by ID |
| GET | `/api/quizzes` | Get all quizzes (history) |
| DELETE | `/api/quiz/{id}` | Delete quiz by ID |
| GET | `/docs` | Interactive API documentation |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/quiz/generate" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'
```

### Example Response

```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Turing was a British mathematician and computer scientist...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["University of Cambridge", "Bletchley Park"],
    "locations": ["United Kingdom"]
  },
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": ["Harvard", "Cambridge", "Oxford", "Princeton"],
      "answer": "Cambridge",
      "difficulty": "easy",
      "explanation": "Mentioned in the 'Early life' section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine", "Computer science"]
}
```