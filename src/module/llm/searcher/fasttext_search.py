from chromadb import PersistentClient
from gensim.models.fasttext import load_facebook_vectors
from typing import List
import json
import re


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
        self.client = PersistentClient(path=database_path)
        self.model = load_facebook_vectors(model_path)

        # 从本地文件加载数据
        print("从本地文件加载数据...")
        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 将所有文档连接成一个长字符串
        file_text = " ".join([item["document"] for item in data.values()])

        # 按句子拆分本地文件的文本
        knowledge_base = re.split("。|！|？", file_text)

        # 将句子的FastText嵌入添加到数据库
        self.add_to_database(knowledge_base)

        print("数据收集完成。")

    def add_to_database(self, texts: List[str]):
        """
        将给定文本的FastText嵌入添加到数据库。

        参数:
            texts: 文本列表。
        """
        # 为文本生成FastText嵌入
        embeddings = [self.model.get_vector(text) for text in texts]

        # 确保集合存在

        collection_id = "fasttext"
        collection_names = [
            collection.name for collection in self.client.list_collections()
        ]
        print(collection_names)
        if collection_id not in collection_names:
            self.client.create_collection(collection_id)

        # 再次检查集合是否存在
        collection_names = [
            collection.name for collection in self.client.list_collections()
        ]
        print(collection_names)

        # 等待一段时间
        import time

        time.sleep(1)

        self.client._add(
            collection_id=collection_id,
            embeddings=embeddings,
            ids=[str(i) for i in range(len(texts))],
            documents=embeddings,
        )

    def search(self, query: str, size: int) -> List[str]:
        """
        在数据库中搜索与给定查询最相似的文本。

        参数:
            query: 查询文本。
            size: 返回的结果数量。

        返回:
            最相似文本的列表。
        """
        # 为查询生成FastText嵌入
        query_embedding = self.model.get_vector(query)
        result = self.client.query(query_texts=query_embedding, n_results=size)

        # 返回最相似的文本
        return result["documents"]
