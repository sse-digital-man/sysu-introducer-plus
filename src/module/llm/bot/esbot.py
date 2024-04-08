import openai
from typing import List

from .base import BasicBot
from ..bot_kind import BotKind
from utils.config import config
from elasticsearch import Elasticsearch

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class ESBot(BasicBot):
    def __init__(self, kind: BotKind):
        self.__kind = kind
        self._es=Elasticsearch(["http://localhost:9200"])
        self._es_index = "school_library"
        pass

    def essearch(self, p_query, size):
        dsl = {"query": {"match": {"query": p_query}}, "size": size}
        res = self._es.search(index=self._es_index, body=dsl)
        sim_query = "下面是可以参考数据,标签和文本分别对应如下:"
        # 遍历得到前size个相似问题
        for doc in res["hits"]["hits"]:
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            sim_query = sim_query + "\n    " + _query + ":" + _document
        return sim_query
    
    def talk(self, query: str) -> str:
        content= "你现在的任务是找出问题的关键词，下面是一个示例:\n Q:请问一下中山大学在2024年发生了什么? A:中山大学,校史,2024年 \n 现在的问题是"+query
        # 1.预处理问题,得到关键词
        p_query = self._single_call(content , False)
        print("--预处理后得到的关键词为:", p_query)
        
        # 2.使用es查询得到相似问题
        sim_query = self.essearch(p_query, 3)
        print(sim_query)

        # 3.生成最后的交互结果
        final_query = "问题为:"+query+"\n" + sim_query
        return self._single_call(final_query , True)