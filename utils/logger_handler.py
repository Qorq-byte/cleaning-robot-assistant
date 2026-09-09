import logging
import os
from utils.path_tool import get_abs_path
from datetime import datetime

#日志保存的根目录
LOG_ROOT=get_abs_path("logs")

#确保日志的目录存在
os.makedirs(LOG_ROOT,exist_ok=True)

#日志的配置
DEFAULT_LOG_FORMAT=logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s -  %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
        name:str="agent",
        console_level:int=logging.INFO,
        file_level:int=logging.DEBUG,
        log_file:str=None
) -> logging.Logger:
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #避免日志重复输出
    if logger.handlers:
        return logger

    #控制台日志
    console_handler=logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    #文件日志
    if not log_file:
        log_file=os.path.join(LOG_ROOT,f"{datetime.now().strftime('%Y-%m-%d')}.log")

    file_handler=logging.FileHandler(log_file,encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

#快捷获取日志
logger=get_logger()

if __name__=="__main__":
    logger.info("hello world")