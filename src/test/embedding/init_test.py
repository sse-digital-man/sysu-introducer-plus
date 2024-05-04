import unittest
from module.bot.searcher.fasttext_init import FTDataInitializer

class TestFTDataInitializer(unittest.TestCase):

    def setUp(self):
        # 请用你的实际文件路径替换这些占位符
        database_path = "data/chromadb"
        model_path = "cc.zh.300.bin"
        local_file_path = "data/baidu.json"
        print("TestFTSearcher.setUp")
        self.initializer = FTDataInitializer(database_path, model_path, local_file_path)

    def test_true(self):
        print("TestFTDataInitializer.test_true")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
