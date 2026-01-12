"""
Quiz generation using Google Gemini LLM.
Creates quiz questions from Wikipedia article content.
"""

import google.generativeai as genai
import json
from typing import Dict
from app.config import settings

class QuizGenerator:
    """Generates quiz questions using Gemini LLM."""
    
    def __init__(self):
        """Initialize the Gemini API."""
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Use Gemini 2.5 Flash (latest fast free model)
        # Note: Must include 'models/' prefix
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Define the quiz generation prompt
        self.quiz_prompt_template = """You are an expert quiz creator. Create a comprehensive quiz based on the following Wikipedia article.

Article Title: {title}

Article Content:
{content}

Requirements:
1. Create {num_questions} multiple-choice questions
2. Each question must have EXACTLY 4 options
3. Questions should cover different aspects of the article
4. Include a mix of difficulty levels: easy (2-3 questions), medium (3-4 questions), hard (2-3 questions)
5. Ensure all questions and answers are factually accurate based ONLY on the article content
6. DO NOT make up information not present in the article
7. Each question must have a brief explanation

Also suggest 5-7 related Wikipedia topics for further reading.

Return your response in the following JSON format ONLY (no markdown, no extra text):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct option text",
      "difficulty": "easy",
      "explanation": "Brief explanation of why this is correct"
    }}
  ],
  "related_topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}}

Make sure each question is clear, unambiguous, and tests understanding of the article content.
IMPORTANT: Return ONLY the JSON object, no other text before or after.
"""
    
    def generate_quiz(self, title: str, content: str, num_questions: int = 7) -> dict:
        """
        Generate quiz questions from article content.
        
        Args:
            title: Article title
            content: Article text content
            num_questions: Number of questions to generate (5-10)
        
        Returns:
            Dictionary with quiz questions and related topics
        """
        # Validate input
        if not content or len(content) < 200:
            raise ValueError("Article content is too short to generate a quiz")
        
        # Ensure num_questions is in valid range
        num_questions = max(5, min(10, num_questions))
        
        try:
            # Create the prompt
            prompt = self.quiz_prompt_template.format(
                title=title,
                content=content,
                num_questions=num_questions
            )
            
            print(f"   📝 Sending prompt to Gemini (length: {len(prompt)} chars)")
            
            # Call Gemini API
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192,
                }
            )
            
            # Extract the text response
            response_text = response.text
            
            print(f"   ✅ Received response from Gemini ({len(response_text)} chars)")
            
            # Parse JSON from response
            quiz_data = self._parse_quiz_response(response_text)
            
            # Validate the quiz data
            validated_quiz = self._validate_quiz(quiz_data, num_questions)
            
            return validated_quiz
            
        except Exception as e:
            print(f"   ❌ Error generating quiz: {str(e)}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _parse_quiz_response(self, response_text: str) -> dict:
        """Parse JSON from Gemini response."""
        try:
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, try parsing entire response
                return json.loads(response_text)
                
        except json.JSONDecodeError as e:
            print(f"   ❌ Failed to parse JSON: {e}")
            print(f"   Response text (first 500 chars): {response_text[:500]}")
            raise Exception("Gemini did not return valid JSON format")
    
    def _validate_quiz(self, quiz_data: dict, expected_questions: int) -> dict:
        """Validate and clean quiz data."""
        validated = {
            'quiz': [],
            'related_topics': []
        }
        
        # Validate questions
        if 'questions' in quiz_data and isinstance(quiz_data['questions'], list):
            for q in quiz_data['questions']:
                # Ensure question has all required fields
                if all(key in q for key in ['question', 'options', 'answer', 'difficulty', 'explanation']):
                    # Ensure options is a list of 4 items
                    if isinstance(q['options'], list) and len(q['options']) == 4:
                        # Ensure answer is one of the options
                        if q['answer'] in q['options']:
                            # Ensure difficulty is valid
                            if q['difficulty'].lower() in ['easy', 'medium', 'hard']:
                                validated['quiz'].append({
                                    'question': str(q['question']).strip(),
                                    'options': [str(opt).strip() for opt in q['options']],
                                    'answer': str(q['answer']).strip(),
                                    'difficulty': q['difficulty'].lower(),
                                    'explanation': str(q['explanation']).strip()
                                })
        
        # Validate related topics
        if 'related_topics' in quiz_data and isinstance(quiz_data['related_topics'], list):
            validated['related_topics'] = [str(topic).strip() for topic in quiz_data['related_topics']][:7]
        
        # Check if we have enough questions
        if len(validated['quiz']) < 3:
            raise Exception(f"Generated only {len(validated['quiz'])} valid questions, need at least 3")
        
        print(f"   ✅ Validated {len(validated['quiz'])} questions")
        
        return validated