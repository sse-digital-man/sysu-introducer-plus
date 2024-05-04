import unittest
from module.bot.searcher.fasttext_search import FTSearcher


class TestFTSearcher(unittest.TestCase):

    def setUp(self):
        # 请用你的实际文件路径替换这些占位符
        database_path = "data/chromadb"
        model_path = "cc.zh.300.bin"
        local_file_path = "data/baidu.json"

        self.searcher = FTSearcher(database_path, model_path, local_file_path)

    def test_search(self):
        # query = "中山大学校史."
        size = 1
        # results = self.searcher.search(query, size)
        # print(results)
        # self.assertEqual(len(results), size)  # 检查结果的数量是否正确
        # self.assertIsInstance(results[0], str)  # 检查结果是否是字符串
        queries = [
            "中大的校长是谁？",
            "中山大学在1944年发生了什么大事？",
            "中山医科大学和中山大学有什么关系？",
            "多少分可以进中山大学？",
            "中山大学有几个校区？",
            "中山大学珠海校区有哪些院系？",
            "介绍一下中法核",
            "想了解一下中山大学的转专业政策",
            "中大校歌是啥？",
            "中大的校庆是哪一天？",
            "中大有哪些附属医院？",
            "中山大学的王牌专业是哪一些？",
            "介绍一下校徽，有哪些具体含义？",
            "能简单介绍一下校训吗？",
            "想了解一下中大的二次遴选政策",
            "中大的转专业难度大吗？",
            "中大有哪些知名校友？",
            "为什么推荐报考中大？",
            "中大的吉祥物是什么？有什么具体含义？",
            "中大有哪些学部？",
            "中大历年的校长是谁？",
            "珠海校区是什么时候发展起来的？",
            "介绍一下三地五校区的发展规划",
            "哈哈哈哈哈",
            "主播好帅",
            "国际学生政策是怎样的？",
            "学生社团有哪些？",
            "中山大学的校园文化如何？",
            "有哪些交流项目？",
            "学生宿舍环境如何？",
            "图书馆资源丰富吗？",
            "中山大学的教授们有哪些突出的研究成果？",
            "有哪些奖学金政策？",
            "提供哪些辅导和咨询服务？",
            "就业指导服务如何？",
            "中山大学的校园食堂如何？",
            "体育设施完善吗？",
            "有哪些特色课程？",
            "中山大学的研究生教育如何？",
            "中山大学的学生可以进行哪些实习和实践活动？",
            "校园安全措施如何？",
            "可以参与哪些志愿者活动？",
            "学生如何评价他们的学习经历？",
            "有哪些休闲和娱乐活动？",
            "中山大学对于创新创业有哪些支持？",
            "如何平衡学习和生活？",
            "中山大学的学生如何评价他们的教授？",
            "上课会收手机吗？",
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
