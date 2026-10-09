"""向量数据库"""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag.embedding import EmbeddingModel
from backend.rag.loader import DocumentLoader
from backend.rag.spliter import DocumentSplitter
from backend.config import VectorConfig,vector_config


class VectorStore():
    def __init__(
        self,
        config:VectorConfig=vector_config,
        splitter: DocumentSplitter|None =None,
        embedding_model=None,
        loader:DocumentLoader|None=None,

    ):
        self.config = config
        self.spliter = splitter or DocumentSplitter() # 分割器
        self.embedding_model=embedding_model or EmbeddingModel().create_embedding() # 嵌入模型
        self.loader= loader or DocumentLoader() # 加载器
        self.vectorstore = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding_model,
            persist_directory=config.persist_directory,
        )   # 向量数据库

    def visualize_vectorstore(self):
        """可视化向量数据库"""
        data = self.vectorstore.get(
            include=["documents", "metadatas", "embeddings"]
        )
        result = []
        ids = data.get("ids", [])
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        embeddings = data.get("embeddings", [])
        for i in range(len(ids)):
            chunk = {
                "id": ids[i],
                # 文本内容（防止太长）
                "document": (
                    documents[i][:100] + "..."
                    if len(documents[i]) > 100
                    else documents[i]
                ),
                # 向量维度
                "embedding_dim": (
                    len(embeddings[i])
                    if embeddings is not None
                    else 0
                ),
                # metadata
                "metadata": metadatas[i]
            }
            result.append(chunk)
        return result

    def add_file(self,file_obj):
        # print(f"文件：{file_obj}")
        # 1.文本加载
        docs=self.loader.load(
            file_path=file_obj.file_path,
            file_type=file_obj.file_type
        )
        # print(f"文件：{docs}")

        # 2.文本切分为chunk
        chunks = self.spliter.split(
            docs=docs,
            file_obj=file_obj
        )  # list[Doc]
        # print(spliter)

        # 3.转化为向量,向量存储
        return self.add_chunks(chunks)

    def add_chunks(self,docs:list[Document])->list[str]:
        return self.vectorstore.add_documents(docs) #返回每个文档chunk对应的ID列表
