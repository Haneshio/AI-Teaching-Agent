"""文件上传业务逻辑"""
import os.path
from fastapi import UploadFile, HTTPException
import hashlib
from backend.utils.file_utils import calculate_md5,save_bytes,build_hashed_filename
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.document_crud import add_file,FileMetaCreate,get_file_md5
from pathlib import Path
from backend.services.konwledge_service import vectorize_and_store_text
from backend.config import upload_config

'''文件合法性验证'''
def validate_upload_file(file: UploadFile)->None:
    # 类型验证
    if file.content_type not in upload_config.allowed_types:
        raise HTTPException(status_code=400,detail="不支持的文件类型")    # 客户端请求错误

    # 文件名为空验证
    if not file.filename:
        raise HTTPException(status_code=400,detail="文件名不能为空")

'''读取文件内容'''
async def read_upload_file(file: UploadFile)->bytes:
    '''
    读取文件内容，并验证
    :param file: 文件,UploadFile类型
    :return: 返回文件内容（字节形式）
    '''
    content = await file.read()  # 字节

    # 如果文本内容为空
    if not content:
        raise HTTPException(status_code=400,detail="文件不能为空")

    # 如果文本内容长度超过限制
    max_file_size=upload_config.max_file_size
    if len(content)>max_file_size:
        raise HTTPException(status_code=413,detail="文件大小超过限制")

    return content

'''保存上传的文件'''
def save_upload_file(file:UploadFile,file_hash:str,content:bytes)->str:
    # 判断文件名是否为空
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    # 创建path对象的文件上传目录路径
    upload_dir=Path(upload_config.upload_dir)
    # 获取文件后缀名,并拼接要保存的文件名
    save_filename=build_hashed_filename(file_hash,file.filename)
    # 将文件目录路径与文件名进行拼接
    file_path = upload_dir / save_filename  # 拼接../upload/file_hash.后缀名

    saved_path=save_bytes(content,file_path)
    return saved_path

'''返回成功响应的函数'''
def  build_file_response(file_obj,chunk_count:int,duplicate:bool=False)->dict:
    return {
        "document_id": file_obj.id,  # 文档 ID，用于后续查询、删除、展示引用来源。
        "filename": file_obj.filename,  # 原始文件名，前端展示用。
        "file_type": file_obj.file_type,  # 文件类型，例如 txt / md / pdf。
        "file_size": file_obj.file_size,  # 文件大小，单位 bytes。
        "file_hash": file_obj.file_hash,  # 文件内容哈希值，用于去重。
        "status": "processed",  # 处理状态，例如 uploaded / processing / processed / failed。
        "chunk_count": chunk_count,  # 切分出的 chunk 数量。
        "duplicate": duplicate,  # 是否重复上传。
        "message": "上传并处理成功"  # 给前端展示的提示信息。
    }

'''文件上传函数'''
async def upload(file:UploadFile,db:AsyncSession )->dict:
    # 1、文件类型校验
    validate_upload_file(file)

    # 2、读取文本内容，并计算文件大小和md5
    content=await read_upload_file(file)    # 读取文件内容（bytes），并判断是否为空
    file_len=len(content)               # 计算文件大小
    file_hash=calculate_md5(content)    # 生成md5值

    # 4.判断是否重复
    # 未重复则上传该文件，并将该文件的元数据上传
    if await get_file_md5(file_hash,db): #如果重复
        raise HTTPException(status_code=409,detail="请勿重复上传")

    # 5.没有重复，则保存原始文件
    file_path = save_upload_file(file, file_hash, content)

    # 6.将文件元数据保存到数据库中
    # 创建文件元数据
    filemeta = FileMetaCreate(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_len,
        file_hash=file_hash
    )
    # 将文件元数据添加到数据库中
    file_obj=await add_file(filemeta, db)

    # 7.调用知识库模块，进行文本切分和向量化
    try:
        chunk_count=await vectorize_and_store_text(file_obj)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    # 返回接口数据
    return build_file_response(file_obj,chunk_count)