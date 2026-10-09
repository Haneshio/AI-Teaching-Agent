"""知识库模块业务逻辑"""
from backend.rag.vectorstore import VectorStore
import dotenv
dotenv.load_dotenv()
'''将文本切分，并进行向量化存储'''
async def vectorize_and_store_text(file_obj):
    '''
    记载文本，将文本切分，并进行向量化存储
    :param text: 原始文件存储路径
    :param file_type:文件类型
    :return:
    '''
    vectorstore = VectorStore()
    return vectorstore.add_file(file_obj)

