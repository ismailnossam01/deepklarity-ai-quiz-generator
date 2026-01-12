"""
Database models for storing quiz data.
Defines the structure of the Quiz table in PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Quiz(Base):
    """
    Quiz model - represents a Wikipedia article quiz in the database.
    Each row stores one complete quiz with all questions.
    """
    __tablename__ = "quizzes"
    
    # Primary key - unique ID for each quiz
    id = Column(Integer, primary_key=True, index=True)
    
    # Wikipedia article information
    url = Column(String(500), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    
    # Extracted entities (stored as JSON)
    # Example: {"people": ["Alan Turing"], "organizations": [...]}
    key_entities = Column(JSON, nullable=True)
    
    # Article sections (stored as JSON array)
    # Example: ["Early life", "World War II", "Legacy"]
    sections = Column(JSON, nullable=True)
    
    # Quiz questions (stored as JSON array)
    # Each question has: question, options, answer, difficulty, explanation
    quiz = Column(JSON, nullable=False)
    
    # Related topics for further reading (stored as JSON array)
    # Example: ["Cryptography", "Enigma machine"]
    related_topics = Column(JSON, nullable=True)
    
    # Optional: Store raw HTML for reference
    raw_html = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        """String representation of Quiz object."""
        return f"<Quiz(id={self.id}, title='{self.title}', questions={len(self.quiz)})>"