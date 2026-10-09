"""获取向量模型"""
from langchain_community.embeddings import DashScopeEmbeddings
from backend.config import embedding_config,EmbeddingConfig
import dotenv
dotenv.load_dotenv()

class EmbeddingModel:
    def __init__(self,config:EmbeddingConfig=embedding_config):
        self.config = embedding_config.model

    def create_embedding(self):
        return DashScopeEmbeddings(
            model=self.config,
        )

