import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader,PyPDFLoader
def get_file_md5_hex(filepath:str):#获取文件md5

    if not os.path.exists(filepath):
        logger.error(f"文件不存在:{filepath}")
        return

    if not os.path.isfile(filepath):
        logger.error(f"不是文件:{filepath}")
        return

    md5_obj=hashlib.md5()

    chunk_size=4096
    try:
        with open(filepath,"rb") as f:
            while chunk:=f.read(chunk_size):
                md5_obj.update(chunk)

            md5_hex=md5_obj.hexdigest()
            return md5_hex

    except Exception as e:
        logger.error(f"获取文件md5失败:{filepath},{str(e)}")
        return  None

def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):
    files=[]

    if not os.path.exists(path):
        logger.error(f"目录不存在:{path}")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(filepath:str,passwd=None) -> list[ Document]:
    return PyPDFLoader(filepath,passwd).load()

def text_loader(filepath:str) -> list[ Document]:
    return TextLoader(filepath,encoding="utf-8").load()
txt_loader = text_loader