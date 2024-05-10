from typing import Dict, List
from .interface import SearcherInterface
from elasticsearch import Elasticsearch
from ..kind import SearcherKind
import json

class EsSearcher(SearcherInterface):
    def __init__(self):
        self._es = Elasticsearch(["http://localhost:9200"])
        self._es_index = "school_library"
        self.build_index()

    def search(self, query: str, size: int) -> List[str]:
        """使用elasticsearch搜索返回与 query 相似的文本列表
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            List[str]: 文本列表 [text1, text2, text3, ...]
        """
        dsl = {"query": {"match": {"query": query}}, "size": size}
        search_res = self._es.search(index=self._es_index, body=dsl)
        res = []
        # 遍历得到前size个相似问题
        for doc in search_res["hits"]["hits"]:
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            res.append(_query + ":" + _document)
        return res
    

    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        """返回与 query 相似的文本列表，以及对应的标签信息(query/id)
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            Dict[str, str]: 文本字典 { query1: text1, query2: text2, ...}
        """
        dsl = {"query": {"match": {"query": query}}, "size": size}
        search_res = self._es.search(index = self._es_index, body=dsl)
        res = {}
        # 遍历得到前size个相似问题
        for doc in search_res["hits"]["hits"]:
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            res[_query] = _document
        return res



    def build_index(self)-> bool:
        """基于数据库建立es索引
            Returns:
            bool: 是否之前就存在es索引,没有索引就建立
        """
        if self._es.indices.exists(index=self._es_index):
            return True
        else :
            self._es.indices.delete(index=self._es_index)
            self._es.indices.create(index=self._es_index)
            with open("data\database.json", "r", encoding="utf-8") as f:
                _dict = json.load(f)
            for _, dict in _dict.items():
                self._es.index(index=self._es_index, body=dict)
            return False
    
    def _load_config(self):
        ...