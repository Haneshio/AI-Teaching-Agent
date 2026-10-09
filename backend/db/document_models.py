"""数据表结构"""
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import func, DateTime, String, Float, VARCHAR,Integer
from datetime import datetime

# 1、创建基类
class Base(DeclarativeBase):
    create_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now(),comment="更新时间")

# 2.创建模板类
class FileMeta(Base):
    __tablename__="filemeta"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    filename:Mapped[str]=mapped_column(String(255),comment="文件名")
    file_path:Mapped[str]=mapped_column(String(255),comment="文件路径")
    file_type:Mapped[str]=mapped_column(String(100),comment="文件类型")
    file_size:Mapped[str]=mapped_column(Integer,comment="文件大小")
    file_hash:Mapped[str]=mapped_column(String(255),comment="文件md5值")
