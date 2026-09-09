import random

from nltk.tbl import feature
from ollama import generate

from utils.config_handler import agent_conf
from langchain_core.tools import tool
import os
from rag.rag_service import RagSummarizeService
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
rag = RagSummarizeService()
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
month_arr=["2025-01","2025-02", "2025-03", "2025-04",
           "2025-05", "2025-06", "2025-07", "2025-08",
           "2025-09", "2025-10", "2025-11", "2025-12"]
external_data={}

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return f"城市{city}的天气是晴天，气温23度，空气湿度 78%,南风1级，AQI21，最近6小时降雨概率低"


@tool(description="随机获取用户当前所在城市，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州", "深圳"])

@tool(description="获取用户的id，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)

@tool(description="获取用户当前时间，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)

def generate_external_data():
    if not external_data:
        external_data_path=get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在:{external_data_path}")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time:str=arr[5].replace('"', "")

                external_data[user_id] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }

@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回，如果为检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"未找到用户{user_id}在{month}的记录")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成场景动态注入上下问信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report以调用"


if __name__ == '__main__':
    print(fetch_external_data("1001", "2025-01"))