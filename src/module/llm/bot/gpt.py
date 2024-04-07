import openai
from typing import List

from .base import BasicBot
from ..bot_kind import BotKind
from utils.config import config
from elasticsearch import Elasticsearch

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class GPTBot(BasicBot):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__(BotKind.GPT)
        api_key, url = GPTBot.__get_config()

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=url,
            timeout=5
        )

    def _load_config(self):
        api_key, url = GPTBot.__get_config()

        self.client.api_key = api_key
        self.client.base_url = url

        print(self.client.api_key)
        print(self.client.base_url)

    @staticmethod
    def __get_config():
        info = config.get_system_module("llm", "gpt")
        return info['apiKey'], info['url']

    def _single_call(self, query: str) -> str:
        # 1.预处理问题,得到关键词
        messages = [
            {
                "role": "system",
                "content": "你现在的任务是找出问题的关键词，下面是一个示例:Q:请问一下中山大学在2024年发生了什么? A:中山大学,校史,2024年"
            }, {
                "role": "user",
                "content": query
            }
        ]
        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )
        p_query = response.choices[0].message.content
        print("--预处理后得到的关键词为:", p_query)
        
        # 2.使用es查询得到相似问题
        es = Elasticsearch(["http://localhost:9200"])
        indexname = "school_library"
        dsl = {"query": {"match": {"query": p_query}}, "size": 3}
        res = es.search(index=indexname, body=dsl)
        final_query = "下面是可以参考数据,标签和文本分别对应如下:"
        # 遍历得到前5个相似问题
        for doc in res["hits"]["hits"]:
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            final_query = final_query + "\n    " + _query + ":" + _document
        print(final_query)

        # 3.生成最后的交互结果
        messages = [
            {
                "role": "system",
                "content": BasicBot.system_prompt
            }, {
                "role": "user",
                "content": "问题为:"+query+"\n"+final_query
            }
        ]
        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )
        return response.choices[0].message.content