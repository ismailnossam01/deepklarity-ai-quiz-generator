"""
Pydantic schemas for API request and response validation.
Defines the structure of data sent to and from the API.
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional
from datetime import datetime

# Schema for a single quiz question
class QuizQuestion(BaseModel):
    """Represents one question in the quiz."""
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="Four answer options (A-D)")
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(..., description="Explanation of the correct answer")

# Schema for key entities extracted from article
class KeyEntities(BaseModel):
    """Named entities found in the article."""
    people: List[str] = Field(default_factory=list, description="People mentioned")
    organizations: List[str] = Field(default_factory=list, description="Organizations mentioned")
    locations: List[str] = Field(default_factory=list, description="Locations mentioned")

# Schema for API request - when user submits a URL
class QuizGenerateRequest(BaseModel):
    """Request body for generating a new quiz."""
    url: str = Field(..., description="Wikipedia article URL", example="https://en.wikipedia.org/wiki/Alan_Turing")

# Schema for API response - complete quiz data
class QuizResponse(BaseModel):
    """Complete quiz response with all data."""
    id: int = Field(..., description="Unique quiz ID")
    url: str = Field(..., description="Wikipedia article URL")
    title: str = Field(..., description="Article title")
    summary: Optional[str] = Field(None, description="Article summary")
    key_entities: Optional[KeyEntities] = Field(None, description="Extracted entities")
    sections: Optional[List[str]] = Field(None, description="Article sections")
    quiz: List[QuizQuestion] = Field(..., description="List of quiz questions")
    related_topics: Optional[List[str]] = Field(None, description="Related topics for further reading")
    created_at: Optional[datetime] = Field(None, description="When quiz was created")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allow creating from ORM models

# Schema for history list - simplified version
class QuizListItem(BaseModel):
    """Simplified quiz info for history list."""
    id: int
    url: str
    title: str
    created_at: Optional[datetime] = None
    question_count: int = 0
    
    class Config:
        from_attributes = True