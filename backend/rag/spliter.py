from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.config import splitter_config, SplitterConfig


class DocumentSplitter():
    def __init__(self,config:SplitterConfig=splitter_config):
        self.config=config
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=config.length_function,
        )


    def split(self,docs:list[Document],file_obj)->list[Document]:
        # 分割
        chunks=self.splitter.split_documents(docs)
        # 存储metadata
        for index,chunk in enumerate(chunks):
            chunk.metadata.update({
                "file_id": file_obj.id,  # 文件id
                "filename": file_obj.filename,  # 前端展示文件来源
                "file_type": file_obj.file_type,  # 文件类型
                # "page": None,  # 页码
                "chunk_index": index  # 用于知道是第几个文本块。
            })
        # print(f"分割：{chunks}")
        return chunks

