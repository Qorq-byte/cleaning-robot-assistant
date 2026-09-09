from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

def load_system_prompts():
    try:
        system_prompt_path=get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置中没有找到main_prompt_path字段")
        raise  e

    try:
        return open(system_prompt_path,'r',encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词错误，{str(e)}")
        raise e

def load_rag_prompts():
    try:
        rag_prompt_path=get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置中没有找到rag_summarize_prompt_path字段")
        raise  e

    try:
        return open(rag_prompt_path,'r',encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析rag提示词错误，{str(e)}")
        raise e

def load_report_prompts():
    try:
        report_prompt_path=get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置中没有找到report_prompt_path字段")
        raise  e

    try:
        return open(report_prompt_path,'r',encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告提示词错误，{str(e)}")
        raise e

if __name__=="__main__":
    print(load_system_prompts())
