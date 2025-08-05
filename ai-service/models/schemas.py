from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    documents: str
    questions: List[str]

class QuestionResponse(BaseModel):
    answers: List[str]

class ChatMessage(BaseModel):
    message: str
    timestamp: str = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str = None
