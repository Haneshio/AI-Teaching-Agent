from io import BytesIO
import pytest
from fastapi import UploadFile, HTTPException
from backend.services.upload_service import *
from starlette.datastructures import Headers

# 手动创建一个假的 UploadFile
def make_upload_file(filename:str|None,content:bytes,content_type:str)->UploadFile:
    file=UploadFile(
        filename=filename,
        file=BytesIO(content),  #把 bytes 内容伪装成一个“文件流”。
        headers=Headers({'Content-Type':content_type})
    )
    return file

'''测试 validate_upload_file'''
def test_validate_upload_file_success():
    file=make_upload_file("test.txt",b"hello","text/plain")
    validate_upload_file(file)

def test_validate_upload_file_empty_filename():
    file=make_upload_file("",b"hello","text/plain")
    with pytest.raises(HTTPException) as e:
        validate_upload_file(file)
    assert e.value.status_code == 400

def test_validate_upload_file_invalid_content_type():
    file=make_upload_file("test.pptx",b"hello","application/vnd.openxmlformats-officedocument.presentationml.presentation")
    with pytest.raises(HTTPException) as e:
        validate_upload_file(file)
    assert e.value.status_code==400

'''测试read_upload_file'''
@pytest.mark.asyncio # 表示是一个一部测试
async def test_read_upload_file_success():
    file=make_upload_file("test.txt",b"hello","text/plain")
    result=await read_upload_file(file)
    assert result==b"hello"

@pytest.mark.asyncio
async def test_read_upload_file_empty_content():
    file=make_upload_file("test.txt",b"","text/plain")
    with pytest.raises(HTTPException) as e:
        await read_upload_file(file)
    assert e.value.status_code==400

@pytest.mark.asyncio
async def test_read_upload_file_file_too_large(monkeypatch): #pytest提前准备好的工具对象
    file=make_upload_file("test.txt",b"hello World","text/plain")
    monkeypatch.setattr(upload_config,"max_file_size",5)  #临时修改max_upload_size值
    with pytest.raises(HTTPException) as e:
        await read_upload_file(file)
    assert e.value.status_code==413

'''测试save_upload_file'''
def test_save_upload_file_success(monkeypatch,tmp_path):
    file=make_upload_file("test.txt",b"hello","text/plain")
    monkeypatch.setattr(upload_config,"upload_dir",tmp_path)    # 设置临时upload_dir
    result=save_upload_file(file, "abc123", b"hello")
    assert Path(result).exists()
    assert Path(result).read_bytes() == b"hello"
    assert Path(result).name=="abc123.txt"

def test_save_upload_file_empty_filename(monkeypatch,tmp_path):
    file=make_upload_file("",b"hello","text/plain")
    monkeypatch.setattr(upload_config, "upload_dir", tmp_path)
    with pytest.raises(HTTPException) as e:
        save_upload_file(file, "abc123", b"hello")
    assert e.value.status_code==400

'''测试build_file_response'''
# def test_build_file_response(monkeypatch,tmp_path):
#     file=make_upload_file("test.txt",b"hello","text/plain")
