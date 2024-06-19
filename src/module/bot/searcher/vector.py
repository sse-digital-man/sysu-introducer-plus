from typing import Dict, List, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import json

from .interface import SearcherInterface


class VectorSearcher(SearcherInterface):
    def __init__(self):
        super().__init__()
        # 定义llm_chain和vector_store
        self.__vector_store = None
        self.__prompt_template = """请回答用户关于中山大学信息的查询\n查询: {query}\n回答: {answer}"""


    def handle_starting(self):
        # 获取openai的embedding实例
        base_embeddings = OpenAIEmbeddings(openai_api_key = self.__openai_api_key, openai_api_base = self.__openai_api_base)
        
        # vectorstore实例化
        self.__vector_store = Chroma(persist_directory = 'data/vectorstores', embedding_function = base_embeddings)

        # 建立索引
        self.build_index()


    def similarity_search(self, query: str, size: int) -> List[Tuple[Document, float]]:
        
        docs = self.__vector_store.similarity_search_with_score(query, k=size)
        return docs


    def search(self, query: str, size: int) -> List[str]:
        """使用elasticsearch搜索返回与 query 相似的文本列表
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            List[str]: 文本列表 [text1, text2, text3, ...]
        """
        docs = self.similarity_search(query, size)

        return [doc[0].metadata['document'] for doc in docs]


    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        """返回与 query 相似的文本列表，以及对应的标签信息(query/id)
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            Dict[str, str]: 文本字典 { query1: text1, query2: text2, ...}
        """
        docs = self.similarity_search(query, size)

        return {doc[0].metadata['query']: doc[0].metadata['document'] for doc in docs}


    def build_index(self) -> bool:
        """基于数据库建立Chroma索引
        Returns:
            bool: 是否之前就存在Chroma索引,没有索引就建立
        """
        # 加载 JSON 文件
        with open("data/database.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # 初始化一个空的文档列表
        documents = []

        # 遍历数据字典中的每一项
        for key, value in data.items():
            # 检查当前的键是否已经存在于元数据列表中
            if not any(item['id'] == str(key) for item in self.__vector_store.get()['metadatas']):
                # 如果不存在，则创建一个新的Document对象
                # 对内容添加 prompt
                page_content = self.__prompt_template.format(query=value['query'], answer=value['document'])
                # 元数据组织
                metadata = {'id': key, 'query': value['query'], 'document': value['document'], 'keyword': value['metadata']}
                # 合成 document
                document = Document(page_content=page_content, metadata=metadata)
                
                # 将新创建的Document对象添加到文档列表中
                documents.append(document)

        # 若没有新的数据，不修改 vector store
        add_doc_count = len(documents)
        if add_doc_count == 0:
            print('No new documents to add to the vector store.')
            return True
        
        # 添加文档到 vector store
        self.__vector_store.add_documents(documents)
        print(f"Added {add_doc_count} documents to the vector store.")

        return False


    def load_config(self):
        info = self._read_config()
        self.__openai_api_key = info["apiKey"]
        self.__openai_api_base = info["url"]