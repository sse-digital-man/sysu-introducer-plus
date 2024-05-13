from . import BasicBot


class SimpleBot(BasicBot):
    def load_config(self):
        pass

    def talk(self, query: str) -> str:
        caller = self._sub_module("caller")
        searcher = self._sub_module("searcher")

        # 如果Searcher为空，直接使用调用器返回
        if searcher is None:
            return caller.single_call(query, True)

        content = (
            "你现在的任务是找出问题的关键词，注意:提取的关键词中需要将“中大”更名为“中山大学”，下面是一个示例:\n"
            "Q:请问一下中大在2024年发生了什么? A:中山大学,校史,2024年 \n"
            "现在的问题是" + query
        )

        # 1.预处理问题,得到关键词
        p_query = caller.single_call(content, False)
        # print("--预处理后得到的关键词为:", p_query)

        # 2.使用es查询得到相似问题
        sim_query = searcher.search(p_query, 3)
        # print(sim_query)

        # 3.生成最后的交互结果
        final_query = (
            "请回答问题:"
            + query
            + "下面是参考资料,如果参考资料与问题无关,请注意介绍人的身份并礼貌回答:"
        )

        for _id, _query in enumerate(sim_query):
            final_query += "\n参考资料" + str(_id + 1) + ":" + _query
        # print(final_query)

        return caller.single_call(final_query, True)
