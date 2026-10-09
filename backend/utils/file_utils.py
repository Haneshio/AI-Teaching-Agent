"""文件处理工具"""
import hashlib
from pathlib import Path

'''创建目录'''
def create_dir(directory:str|Path)->Path:
    '''
    创建目录
    :param directory:上传文件的保存目录路径
    :return: 返回创建好的文件目录，Path对象的文件上传路径
    '''
    path=Path(directory)
    path.mkdir(parents=True,exist_ok=True)#如果目录不存在就创建，父目录不存在也一起创建；如果目录已经存在，不报错。
    return path

def save_bytes(content:bytes, file_path:str|Path)->str:
    '''
    将字节内容content保存到file_path文件目录中
    :param content:字节内容
    :param file_path:目标文件路径
    :return: 返回文件路径,str
    '''
    path=Path(file_path)
    create_dir(path.parent) # 确认当前文件路径的父目录是否存在
    # 将字节内容写入file_path中
    with open(path,"wb") as f:
        f.write(content)
    return str(path)

'''读取文件后缀名'''
def get_file_suffix(filename:str)->str:
    if not filename:
        raise ValueError("filename不能为空")
    return Path(filename).suffix.lower()

'''拼接存储的文件名'''
def build_hashed_filename(file_hash: str, filename: str) -> str:
    if not file_hash:
        raise ValueError("file_hash不能为空")
    if not filename:
        raise ValueError("filename不能为空")
    return f"{file_hash}{get_file_suffix(filename)}"

'''计算md5值'''
def calculate_md5(text:bytes)->str:
    # 如果文本为空
    if not text:
        raise ValueError("text不能为空")
    return hashlib.md5(text).hexdigest()

if __name__ == '__main__':
    create_dir("./data/ceshi")
    # print(calculate_md5(b"hello"))  #'b'：字节