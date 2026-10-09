"""读取配置文件"""
from dataclasses import dataclass
from pathlib import Path
import dotenv
import os
BASE_DIR = Path(__file__).resolve().parent #__file__:当前Python文件路径,resolve()把路径转换成绝对路径。
dotenv.load_dotenv(BASE_DIR / ".env")

'''文件上传配置'''
class UploadConfig:
    def __init__(self):
        self.upload_dir = "data/uploads"  # 上传文件保存目录
        self.allowed_types=[
            "text/plain",  # txt文档
            "application/pdf",   #pdf文档
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"   # docx
        ] # 可允许上传的文件类型
        self.max_file_size=50*1024*1024 # 文件大小限制，50MB


'''文本切割配置类'''
class SplitterConfig:
    def __init__(self):
        self.chunk_size = 300
        self.chunk_overlap = 50
        self.separators = ['\n', '\n\n', '', ' ', '.', '。', ',', '，', '?', '？']
        self.length_function = len

'''嵌入模型配置类'''
class EmbeddingConfig:
    def __init__(self):
        self.model = "text-embedding-v4"

'''向量数据库配置类'''
class VectorConfig:
    def __init__(self):
        self.collection_name = "ai_teaching_vector"
        self.persist_directory = "data/chroma"

'''Mysql数据库配置类'''
class MySqlConfig:
    def __init__(self):
        self.DB_HOST = os.getenv("MYSQL_HOST")
        self.DB_PORT = os.getenv("MYSQL_PORT")
        self.DB_USER = os.getenv("MYSQL_USER")
        self.DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.DB_DATABASE = os.getenv("MYSQL_DATABASE")

    @property
    def database_url(self)->str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

'''聊天模型配置类'''
@dataclass(frozen=True) # 创建一个不可修改的数据类对象。
class ChatModelConfig:
    model:str="qwen3-max"
    temperature:float=0.2

'''相似检索配置类'''
@dataclass(frozen=True)
class RetrieverConfig:
    search_type:str="similarity"
    k:int=2

mysql_config = MySqlConfig()
upload_config = UploadConfig()
splitter_config = SplitterConfig()
embedding_config = EmbeddingConfig()
vector_config = VectorConfig()
chatmodel_config = ChatModelConfig()
retriever_config = RetrieverConfig()


if __name__ == '__main__':
    mysql_config = MySqlConfig()
    print(mysql_config.database_url)