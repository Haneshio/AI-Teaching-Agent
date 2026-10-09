import pytest
from backend.utils.file_utils import *

def test_get_file_suffix():
    assert get_file_suffix('test.txt') == '.txt'
    assert get_file_suffix('test.pdf') == '.pdf'
    assert get_file_suffix('test.docx') == '.docx'
    assert get_file_suffix("README") == ""
    assert get_file_suffix("course.note.txt") == ".txt"

def test_get_file_suffix_empty_filename():
    with pytest.raises(ValueError):
        get_file_suffix("")


def test_build_hashed_filename():
    assert build_hashed_filename('abc123','test.txt') == 'abc123.txt'

def test_build_hased_filename_empty_hash():
    with pytest.raises(ValueError):
        build_hashed_filename("","test.txt")

def test_build_hased_filename_empty_filename():
    with pytest.raises(ValueError):
        build_hashed_filename("abc123","")

def test_calculate_md5():
    assert calculate_md5(b"hello")=="5d41402abc4b2a76b9719d911017c592"

def test_calculate_md5_empty_text():
    with pytest.raises(ValueError):
        calculate_md5(b"")

def test_create_dir(tmp_path): #tmp_path:pytest的自动临时目录
    directory=tmp_path/"uploads"
    result=create_dir(directory)

    assert result.exists() # 判断路径是否存在
    assert result.is_dir() # 判断路径是否为目录
    assert result==directory

def test_create_dir_nested(tmp_path): # 测试多层嵌套目录创建
    directory=tmp_path/"data"/"uploads"
    result=create_dir(directory)
    assert result.exists()
    assert result.is_dir()
    assert result==directory

def test_save_bytes(tmp_path):
    directory=tmp_path/"uploads"/"test.txt"
    content=b"hello"
    result=save_bytes(content,directory)
    assert Path(result).exists()
    assert Path(result).is_file()
    assert Path(result).read_bytes()==b"hello"
    assert result==str(directory)
