import chromadb
from gensim.models.fasttext import load_facebook_vectors
import json


class FTDataInitializer:
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
        # 创建集合
        collection_id = "fasttext"
        self.collection = self.client.get_or_create_collection(name=collection_id)

        self.model = load_facebook_vectors(model_path)

        # 从本地文件加载数据
        print("从本地文件加载数据...")
        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.documents = []
        self.metadatas = []

        for key, value in data.items():
            self.documents.append(value["document"])
            metadata_str = value["metadata"]
            metadata_dict = {key: True for key in metadata_str.split(",")}
            self.metadatas.append(metadata_dict)

        self.embeddings = [
            self.model.get_vector(text).tolist() for text in self.documents
        ]

        self.collection.add(
            embeddings=self.embeddings,
            documents=self.documents,
            metadatas=self.metadatas,
            ids=[str(i) for i in range(len(self.documents))],
        )

        print("数据收集完成。")
