import os
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List, Optional
from models.schemas import QuestionRequest, QuestionResponse, ChatMessage, ChatResponse
from services.gemini_service import GeminiService
import asyncio
from datetime import datetime

router = APIRouter()
gemini_service = GeminiService()

# Expected API key for authentication
EXPECTED_API_KEY = os.getenv("API_SERVICE_KEY", "hackrx-secret-key-2024")

async def verify_api_key(authorization: Optional[str] = Header(None)):
    """API key verification"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    # Extract the token
    token = authorization.replace("Bearer ", "")
    
    # Verify against expected API key
    if token != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return authorization

@router.post("/hackrx/run", response_model=QuestionResponse)
async def process_questions(
    request: QuestionRequest,
    authorization: str = Depends(verify_api_key)
):
    """
    Process questions using your trained Discovery Engine and Gemini AI
    Note: The 'documents' field is ignored as you have pre-trained data in Google Cloud
    """
    try:
        if not request.questions:
            raise HTTPException(status_code=400, detail="At least one question is required")
        
        # Process questions using your Discovery Engine + Gemini service
        # The document_url parameter is not used since you have pre-trained data
        answers = await gemini_service.answer_questions(
            document_url="",  # Not used - your data is in Discovery Engine
            questions=request.questions
        )
        
        return QuestionResponse(answers=answers)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    message: ChatMessage,
    authorization: str = Depends(verify_api_key)
):
    """
    Chat endpoint that uses your Discovery Engine knowledge base
    """
    try:
        if not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Generate response using Discovery Engine + Gemini service
        response_text = await gemini_service.chat_response(message.message)
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "ai-service", 
        "timestamp": datetime.now().isoformat(),
        "discovery_engine": {
            "project_id": gemini_service.project_id,
            "engine_id": gemini_service.engine_id,
            "location": gemini_service.location
        }
    }
