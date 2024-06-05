from . import BasicBot


class HydeBot(BasicBot):
    def load_config(self):
        pass

    @BasicBot._handle_log
    def talk(self, query: str) -> str:
        caller = self._sub_module("caller")
        searcher = self._sub_module("searcher")

        # 如果Searcher为空，直接使用调用器返回
        if searcher is None:
            return caller.single_call(query, True)


        # 2.使用es查询得到相似问题
        sim_query = searcher.search(query, 3)

        demonstrate_prompt = """
### 示范一
[用户问题]
国际学生政策是怎样的？
[参考资料]
参考资料1:
标题:国际学生政策
内容:详情可见中山大学留学生办公室官网
[回答]
国际学生政策，官网有最权威的信息哦！快去中山大学留学生办公室官网看看吧，你会有新发现的！

### 示范二
[用户问题]
可以介绍一下你自己嘛？
[参考资料]
参考资料1:
标题:中山大学校校歌歌词
内容:白云山高,珠江水长,吾校矗立,蔚为国光,中山手创
[回答]
嗨！我是中小大，中大软件工程学院的大二学生，也是校史介绍官。我超爱写代码和阅读历史书籍！

### 示范三
[用户问题]
为什么皮卡丘喜欢放电
[参考资料]
参考资料1:
标题:中山大学的微电子科学与技术学院本科招生专业
内容:微电子科学与工程
参考资料2:
标题:中山大学的集成电路学院本科招生专业
内容:微电子科学与工程
[回答]
很抱歉，我只是一个校史介绍官，不能回答关于皮卡丘的问题哦~

### 开始任务
"""

        final_query = demonstrate_prompt + "\n[用户问题]\n" + query + "\n[参考资料]"

        for _id, _query in enumerate(sim_query):
            final_query += "\n参考资料" + str(_id + 1) + ":\n" + _query

        return caller.single_call(final_query, True)
