import unittest
import psutil
from module.bot.searcher.fasttext import FTSearcher


class TestFTSearcher(unittest.TestCase):

    def setUp(self):
        self.searcher = FTSearcher()
        self.searcher.handle_starting()

    def test_search(self):
        size = 1
        queries = [
            "中大的校长是谁？",
            "中山大学在1944年发生了什么大事？",
        ]

        # 获取当前进程的内存占用情况
        process = psutil.Process()
        memory_usage = process.memory_info().rss

        for query in queries:
            results = self.searcher.search(query, size)
            print(f"Query: {query}")
            print("Results:", results)
            self.assertEqual(len(results), size)  # 检查结果的数量是否正确
            self.assertIsInstance(results[0], str)  # 检查结果是否是字符串
            print()

        memory_usage_mb = memory_usage / 1024 / 1024
        print("Memory usage:", memory_usage_mb, "MB")


if __name__ == "__main__":
    unittest.main()
