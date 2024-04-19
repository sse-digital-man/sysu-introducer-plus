import unittest
from ...module.llm.searcher.fasttext_search import FTSearcher


class TestFTSearcher(unittest.TestCase):

    def setUp(self):
        # 请用你的实际文件路径替换这些占位符
        database_path = "data/chromadb"
        model_path = "cc.zh.300.bin"
        local_file_path = "data/baidu.json"

        self.searcher = FTSearcher(database_path, model_path, local_file_path)

    def test_search(self):
        query = "This is a query."
        size = 2
        results = self.searcher.search(query, size)
        self.assertEqual(len(results), size)  # 检查结果的数量是否正确
        self.assertIsInstance(results[0], str)  # 检查结果是否是字符串


if __name__ == "__main__":
    unittest.main()
