from typing import Dict, List
import json
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import os
import re

from .interface import SearcherInterface


class VectorSearcher(SearcherInterface):
    def __init__(self):
        super().__init__()
        # 定义llm_chain和vector_store
        self.__llm_chain = None
        self.__vector_store = None

    def handle_starting(self):
        # Notice: 不能够在 __init__() 中编写除了定义之外的操作
        
        # 定义prompt
        prompt_template = """请回答用户关于中山大学信息的查询，并且把查询连接到回答中\n查询: {query}\n回答: """
        prompt = PromptTemplate(input_variables=["query"], template=prompt_template)
        # 获取llm实例
        llm = OpenAI(temperature=0, openai_api_key=self.__openai_api_key, openai_api_base=self.__openai_api_base)
        # 获取openai的embedding实例
        base_embeddings = OpenAIEmbeddings(openai_api_key = self.__openai_api_key, openai_api_base = self.__openai_api_base)
        
        # llm_chain实例化
        self.__llm_chain = LLMChain(llm=llm, prompt=prompt)
        # vectorstore实例化
        self.__vector_store = Chroma(persist_directory = 'data/vectorstores', embedding_function = base_embeddings)
        # self.build_index()

    def search(self, query: str, size: int) -> List[str]:
        """使用elasticsearch搜索返回与 query 相似的文本列表
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            List[str]: 文本列表 [text1, text2, text3, ...]
        """
        query += '\n' + self.__llm_chain.invoke(query)['text']

        docs = self.__vector_store.similarity_search_with_score(query, k=3)

        pattern = re.compile(r'查询: (.*?)\n回答: (.*)', re.DOTALL)
        doc_list = ['标题:'+pattern.search(doc[0].page_content).group(1) +'\n内容:'+pattern.search(doc[0].page_content).group(2) for doc in docs]

        return doc_list

    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        """返回与 query 相似的文本列表，以及对应的标签信息(query/id)
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            Dict[str, str]: 文本字典 { query1: text1, query2: text2, ...}
        """
        ...

    def build_index(self) -> bool:
        """基于数据库建立Chroma索引
        Returns:
            bool: 是否之前就存在Chroma索引,没有索引就建立
        """
        return False

    def load_config(self):
        info = self._read_config()
        self.__openai_api_key = info["apiKey"]
        self.__openai_api_base = info["url"]
