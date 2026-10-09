"""组装链"""
from langchain_core.runnables import RunnablePassthrough
from backend.rag.retriever import create_retriever
from langchain_core.documents import Document
from backend.rag.prompt import  create_rag_prompt
from backend.rag.model import create_chat_model
from langchain_core.output_parsers import StrOutputParser

def format_func(docs:list[Document])->str:
    if not docs:
        return "未检索到相关参考资料"

    text='['
    for doc in docs:
        text += doc.page_content
    text += ']'
    return text

"""创造链"""
def create_chain(
        retriever=None,
        prompt=None,
        llm=None,
):
    '''
    :param retiever:检索器
    :param prompt:提示词
    :param llm:大模型
    :return:
    '''
    retriever=retriever or create_retriever()
    prompt=prompt or create_rag_prompt()
    llm=llm or create_chat_model()
    # 组装链
    chain=(
        {
            'input':RunnablePassthrough(),
            "context":retriever|format_func
        }
        |prompt
        |llm
        |StrOutputParser()
    )
    return chain

"""用户提问"""
def ask(question:str)->str:
    '''
    :param question: 用户的提问信息
    :return: 返回大模型回答结果
    '''
    chain=create_chain()
    res=chain.invoke(question)
    return res

