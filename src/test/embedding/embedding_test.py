import unittest
from ...module.llm.bot.fasttext_search import FTBot
from ...module.llm.searcher.fasttext_search import FTSearcher


class TestFTSearcher(unittest.TestCase):

    def setUp(self):
        # 请用你的实际文件路径替换这些占位符
        database_path = "data/chromadb"
        model_path = "cc.zh.300.bin"
        local_file_path = "data/baidu.json"

        self.searcher = FTSearcher(database_path, model_path, local_file_path)

    def test_search(self):
        query = "你好"
        size = 10

        # 使用 FTSearcher 搜索文本
        result = self.searcher.search(query, size)

        # 验证搜索结果的数量
        self.assertEqual(len(result), size)

        # 验证搜索结果的类型
        for text in result:
            self.assertIsInstance(text, str)


if __name__ == "__main__":
    unittest.main()
