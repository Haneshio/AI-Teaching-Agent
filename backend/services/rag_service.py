"""rag业务逻辑"""
from backend.rag.chain import ask

async def rag_chat(chat_question:str):
    res=ask(chat_question)
    # print(res)
    return {
        "answer":res,
        "sources":[]
    }
