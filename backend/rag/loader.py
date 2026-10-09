"""文本加载器"""

from langchain_community.document_loaders import TextLoader, Docx2txtLoader,PyPDFLoader
from langchain_core.documents import Document
# from pptx import Presentation
# 文档加载器
class DocumentLoader:
    def __init__(self):
        self.loader_map={
            "text/plain": self._load_txt,
            "application/pdf": self._load_pdf,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": self._load_docx,
            # "application/vnd.openxmlformats-officedocument.presentationml.presentation":self._load_pptx,
        }

    # 文本加载器
    def _load_txt(self,file_path:str):
        return TextLoader(
            file_path,
            encoding='utf-8',
        )

    # pdf加载器
    def _load_pdf(self,file_path:str):
        return PyPDFLoader(
            file_path
        )

    # docx加载器
    def _load_docx(self,file_path:str):
        return Docx2txtLoader(
            file_path
        )

    # # pptx加载器(采用UnstructuredPowerPointLoader/或者自定义loader)
    # def _load_pptx(self,file_path:str):


    # 根据不同的文件类型采用不同的加载器
    def load(self,file_path:str,file_type:str)->list[Document]:
        # print(file_type)
        # 根据文件类型获取加载函数
        loader_cls=self.loader_map.get(file_type)
        # 如果结果为空，则提示错误
        if loader_cls is None:
            raise ValueError(f"不支持的文件类型：{file_type}")
        # 文件加载
        loader = loader_cls(file_path)
        return loader.load()

