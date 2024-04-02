import json
import time
from typing import Dict, List, Any
import chromadb
from gensim.models.fasttext import load_facebook_vectors
from .interface import SearcherInterface
from ..prompt import KEYWORD_EXTRACT_PROMPT
from ..caller.interface import CallerInterface


class FTSearcher(SearcherInterface):
    def __init__(self):
        super().__init__()
        self.database_path = "data/chromadb"
        self.model_path = "cc.zh.300.bin"
        self.local_file_path = "data/database.json"
        self.collection_id = "fasttext"
        self.collection = None
        self.model = None

        self.client = chromadb.PersistentClient(self.database_path)

        self._init_model()

    def _init_model(self):
        # 加载FastText模型
        self.model = load_facebook_vectors(self.model_path)

    def _process(self, query: str) -> Any:
        p_query = self._caller.single_call(KEYWORD_EXTRACT_PROMPT % query, False)
        return p_query

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

    def search_with_label(self, query: str, size: int) -> Dict[str, str]: ...

    def build_database(self) -> bool:
        # 如果集合已经存在，则直接返回collection
        try:
            self.collection = self.client.get_collection(name=self.collection_id)
            print("集合已经存在。")
            return True
        except ValueError:
            print("集合不存在。")

        self.collection = self.client.create_collection(name=self.collection_id)

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
        return False

    def load_config(self): ...

    @property
    def _caller(self) -> CallerInterface:
        return self._sub_module("caller")
