"""读取提示词"""
from langchain_core.prompts import ChatPromptTemplate

def create_rag_prompt()->ChatPromptTemplate:
    prompt=ChatPromptTemplate.from_messages([
        ("system","你是一个AI教学助手，需要根据相关参考资料:{context}对用户的提问进行回答。"),
        ('human',"用户提问：{input}")
        ]
    )
    return prompt
