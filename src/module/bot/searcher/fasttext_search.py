import chromadb
from gensim.models.fasttext import load_facebook_vectors
from typing import List
import time
from .interface import SearcherInterface

class FTSearcher(SearcherInterface):
    """
    使用FastText嵌入在ChromaDB数据库中搜索文本的类。
    """

    def __init__(self, database_path: str, model_path: str, local_file_path: str):
        """
        初始化FTSearcher。

        参数:
            database_path: ChromaDB数据库的路径。
            model_path: FastText模型的路径。
            local_file_path: 从本地文件加载数据的路径。
        """

        self.client = chromadb.PersistentClient(database_path)
        collection_id = "fasttext"
        self.collection = self.client.get_collection(name=collection_id)

        # 加载FastText模型
        print("加载FastText模型...")
        self.model = load_facebook_vectors(model_path)
        print("FastText模型加载完成。")

    def search(self, query: str, size: int) -> List[str]:
        """
        在数据库中搜索与给定查询最相似的文本。

        参数:
            query: 查询文本。
            size: 返回的结果数量。

        返回:
            最相似文本的列表。
        """
        start = time.time()
        query_embedding = self.model.get_vector(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=size
        )
        print("Query time:", time.time() - start)
        # 返回最相似的文本
        return results["documents"][0]

    def _load_config(self):
        pass

    def check(self):
        pass

    def search_with_label(self):
        pass