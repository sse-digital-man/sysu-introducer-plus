import unittest
from module.bot.searcher.fasttext_search import FTSearcher


class TestFTSearcher(unittest.TestCase):

    def setUp(self):
        # 请用你的实际文件路径替换这些占位符

        self.searcher = FTSearcher()

    def test_search(self):
        # query = "中山大学校史."
        size = 1
        # results = self.searcher.search(query, size)
        # print(results)
        # self.assertEqual(len(results), size)  # 检查结果的数量是否正确
        # self.assertIsInstance(results[0], str)  # 检查结果是否是字符串
        queries = [
            "中山大学简介",
            "中山大学成立的校史",
            "中山大学的办学情况,校区分布",
            "中山大学创办时间",
            "中山大学的主管部门",
        ]

        for query in queries:
            results = self.searcher.search(query, size)
            print(f"Query: {query}")
            print("Results:", results)
            self.assertEqual(len(results), size)  # 检查结果的数量是否正确
            self.assertIsInstance(results[0], str)  # 检查结果是否是字符串
            print()


if __name__ == "__main__":
    unittest.main()
