import chromadb
from gensim.models.fasttext import load_facebook_vectors
from typing import List
import json
import time

class FTSearcher:
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

        self.model = load_facebook_vectors(model_path)

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
