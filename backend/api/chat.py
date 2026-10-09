from fastapi import APIRouter
from backend.services.rag_service import rag_chat
from pydantic import BaseModel
router=APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    question:str
    
"""接受用户的问题，返回AI回答"""
@router.post("/api/chat")
async def get_chat(chat_request:ChatRequest):
    return await rag_chat(chat_request.question)
    # return {
    #     "answer":"这是一个测试回答，后续会替换为RAG回答",    #AI 回答
    #     "source":[] # 来源
    # }


