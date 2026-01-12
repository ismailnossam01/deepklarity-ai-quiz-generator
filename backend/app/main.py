"""
FastAPI main application file.
Defines all API endpoints for the Wiki Quiz Generator.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import traceback

from app.database import get_db, init_db
from app.models import Quiz
from app.schemas import QuizGenerateRequest
from app.scraper import WikipediaScraper
from app.quiz_generator import QuizGenerator
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Wiki Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper and quiz generator
scraper = WikipediaScraper()
quiz_gen = QuizGenerator()

@app.on_event("startup")
async def startup_event():
    """Run when application starts - create database tables."""
    print("🚀 Starting Wiki Quiz Generator API...")
    init_db()
    print(f"✅ Server running on http://{settings.APP_HOST}:{settings.APP_PORT}")

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Wiki Quiz Generator API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "/api/quiz/generate",
            "get_quiz": "/api/quiz/{quiz_id}",
            "list_quizzes": "/api/quiz/list",
            "docs": "/docs"
        }
    }

@app.post("/api/quiz/generate")
async def generate_quiz_endpoint(request: QuizGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate a new quiz from a Wikipedia article URL.
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 Received request to generate quiz")
        print(f"URL: {request.url}")
        print(f"{'='*60}\n")
        
        # Step 1: Check if quiz already exists (caching)
        existing_quiz = db.query(Quiz).filter(Quiz.url == request.url).first()
        if existing_quiz:
            print(f"✅ Found cached quiz for: {request.url}")
            return format_quiz_response(existing_quiz)
        
        # Step 2: Scrape Wikipedia article
        print(f"📥 Scraping article: {request.url}")
        scraped_data = scraper.scrape_article(request.url)
        
        print(f"✅ Scraped article: {scraped_data.get('title', 'Unknown')}")
        print(f"   Content length: {len(scraped_data.get('content', ''))} characters")
        
        if not scraped_data.get('content') or len(scraped_data.get('content', '')) < 200:
            raise HTTPException(
                status_code=400, 
                detail="Failed to extract sufficient content from Wikipedia article. The article may be too short or unavailable."
            )
        
        # Step 3: Generate quiz using LLM
        print(f"🤖 Generating quiz using Gemini AI...")
        quiz_data = quiz_gen.generate_quiz(
            title=scraped_data['title'],
            content=scraped_data['content'],
            num_questions=7
        )
        
        print(f"✅ Generated {len(quiz_data['quiz'])} questions")
        
        # Step 4: Save to database
        print(f"💾 Saving to database...")
        new_quiz = Quiz(
            url=scraped_data['url'],
            title=scraped_data['title'],
            summary=scraped_data.get('summary', ''),
            key_entities=scraped_data.get('key_entities', {}),
            sections=scraped_data.get('sections', []),
            quiz=quiz_data['quiz'],
            related_topics=quiz_data.get('related_topics', []),
            raw_html=None  # Don't store raw HTML to save space
        )
        
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        
        print(f"✅ Quiz saved successfully! ID: {new_quiz.id}\n")
        
        # Step 5: Return formatted response
        return format_quiz_response(new_quiz)
    
    except ValueError as e:
        print(f"❌ Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"\n❌ ERROR generating quiz:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"\nFull traceback:")
        print(traceback.format_exc())
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@app.get("/api/quiz/{quiz_id:int}")
async def get_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by ID.
    Used when clicking "Details" in history view.
    MUST BE BEFORE /api/quizzes to avoid route conflict
    """
    try:
        print(f"📖 Fetching quiz ID: {quiz_id}")
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")
        
        return format_quiz_response(quiz)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching quiz {quiz_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quizzes")
async def list_quizzes_endpoint(db: Session = Depends(get_db)):
    """
    Get list of all quizzes for history view.
    CHANGED FROM /api/quiz/list to /api/quizzes to avoid route conflict
    """
    try:
        print("📋 Fetching quiz list...")
        quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
        
        print(f"✅ Found {len(quizzes)} quizzes")
        
        quiz_list = []
        for quiz in quizzes:
            # Calculate question count safely
            question_count = 0
            if quiz.quiz:
                if isinstance(quiz.quiz, list):
                    question_count = len(quiz.quiz)
                elif isinstance(quiz.quiz, dict) and 'questions' in quiz.quiz:
                    question_count = len(quiz.quiz['questions'])
            
            quiz_list.append({
                'id': quiz.id,
                'url': quiz.url,
                'title': quiz.title,
                'created_at': quiz.created_at.isoformat() if quiz.created_at else None,
                'question_count': question_count
            })
        
        return quiz_list
    
    except Exception as e:
        print(f"❌ Error listing quizzes:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quiz/{quiz_id:int}")
async def get_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get list of all quizzes for history view.
    """
    try:
        print("📋 Fetching quiz list...")
        quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
        
        print(f"✅ Found {len(quizzes)} quizzes")
        
        quiz_list = []
        for quiz in quizzes:
            # Calculate question count safely
            question_count = 0
            if quiz.quiz:
                if isinstance(quiz.quiz, list):
                    question_count = len(quiz.quiz)
                elif isinstance(quiz.quiz, dict) and 'questions' in quiz.quiz:
                    question_count = len(quiz.quiz['questions'])
            
            quiz_list.append({
                'id': quiz.id,
                'url': quiz.url,
                'title': quiz.title,
                'created_at': quiz.created_at.isoformat() if quiz.created_at else None,
                'question_count': question_count
            })
        
        return quiz_list
    
    except Exception as e:
        print(f"❌ Error listing quizzes:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/quiz/{quiz_id}")
async def delete_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    """
    Delete a quiz by ID.
    """
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")
        
        db.delete(quiz)
        db.commit()
        
        return {"message": f"Quiz {quiz_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def format_quiz_response(quiz: Quiz) -> dict:
    """
    Format quiz database object into API response.
    """
    # Ensure quiz is a list
    quiz_questions = []
    if quiz.quiz:
        if isinstance(quiz.quiz, list):
            quiz_questions = quiz.quiz
        elif isinstance(quiz.quiz, dict) and 'questions' in quiz.quiz:
            quiz_questions = quiz.quiz['questions']
    
    # Ensure related_topics is a list
    related_topics = []
    if quiz.related_topics:
        if isinstance(quiz.related_topics, list):
            related_topics = quiz.related_topics
    
    # Ensure key_entities is a dict
    key_entities = quiz.key_entities if isinstance(quiz.key_entities, dict) else {}
    
    # Ensure sections is a list
    sections = quiz.sections if isinstance(quiz.sections, list) else []
    
    return {
        'id': quiz.id,
        'url': quiz.url,
        'title': quiz.title,
        'summary': quiz.summary or '',
        'key_entities': key_entities,
        'sections': sections,
        'quiz': quiz_questions,
        'related_topics': related_topics,
        'created_at': quiz.created_at.isoformat() if quiz.created_at else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )