"""检索器"""
from backend.rag.vectorstore import VectorStore
from backend.config import retriever_config,RetrieverConfig
def create_retriever(
    vector_store: VectorStore|None = None,
    config: RetrieverConfig=retriever_config,
):
    store=vector_store or VectorStore()  # 向量数据库
    return store.vectorstore.as_retriever(
        search_kwargs={"k":config.k}
    )
    # 返回相似的检索器
    # print(f"检索器：{res}")
