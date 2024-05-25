import json
import chromadb
from gensim.models.fasttext import load_facebook_vectors
from typing import List
import time
from .interface import SearcherInterface

class FTSearcher(SearcherInterface):
    """
    使用FastText嵌入在ChromaDB数据库中搜索文本的类。
    """

    def __init__(self):
        """
        初始化FTSearcher。

        参数:
            database_path: ChromaDB数据库的路径。
            model_path: FastText模型的路径。
            local_file_path: 从本地文件加载数据的路径。
        """
        super().__init__()
        self.database_path = "data/chromadb"
        self.model_path = "cc.zh.300.bin"
        self.local_file_path = "data/database.json"
        self.collection_id = "fasttext"

        self.client = chromadb.PersistentClient(self.database_path)
        # 加载FastText模型
        print("加载FastText模型...")
        self.model = load_facebook_vectors(self.model_path)
        print("FastText模型加载完成。")

    def handle_starting(self):
        self.build_database()

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

    def load_config(self):
        pass

    def check(self):
        pass

    def search_with_label(self):
        pass

    def build_database(self) -> bool:
        """
        基于数据库建立fasttext向量索引。
        """

        # 如果集合已经存在，则直接返回collection
        #
        # Raises:
        #     ValueError: If the collection does not exist
        try:
            self.collection = self.client.get_collection(name=self.collection_id)
            print("集合已经存在。")
            return True
        except ValueError:
            print("集合不存在。")
            pass

        # 创建集合
        # self.collection = self.client.get_or_create_collection(name=self.collection_id)

        self.collection = self.client.create_collection(name=self.collection_id)

        # 从本地文件加载数据
        print("从本地文件加载数据...")
        with open(self.local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []
        metadatas = []
        queries = []

        for _, value in data.items():
            documents.append(value["document"])
            queries.append(value["query"])
            metadata_str = value["metadata"]
            metadata_dict = {key: True for key in metadata_str.split(",")}
            metadatas.append(metadata_dict)

        embeddings = [self.model.get_vector(text).tolist() for text in queries]

        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=[str(i) for i in range(len(documents))],
        )

        print("数据收集完成。")
        return False
