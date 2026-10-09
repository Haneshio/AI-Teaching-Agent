"""数据库的增删查改操作"""
from pathlib import Path

from backend.db.database import engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.db.document_models import FileMeta
from pydantic import BaseModel
from sqlalchemy import select


class FileMetaCreate(BaseModel):
    filename:str|None
    file_path:str|Path
    file_type:str|None
    file_size:int|None
    file_hash:str|None

'''添加操作'''
async def add_file(file: FileMetaCreate,db:AsyncSession)->FileMeta:
    file_obj=FileMeta(**file.dict())
    db.add(file_obj)
    await db.flush()
    await db.refresh(file_obj)
    return file_obj # 返回File ORM对象

'''查询操作'''
# 查询hash值是否唯一
async def get_file_md5(file_hash:str,db:AsyncSession)->bool:
    result=await db.execute(select(FileMeta).where(FileMeta.file_hash==file_hash))
    result=result.scalar_one_or_none()
    if result is None: # 未重复
        return False
    else:       # 重复了
        return True


# if __name__ == '__main__':
#     engine