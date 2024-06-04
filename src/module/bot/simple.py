from . import BasicBot


class SimpleBot(BasicBot):
    def load_config(self):
        pass

    @BasicBot._handle_log
    def talk(self, query: str) -> str:
        caller = self._sub_module("caller")
        searcher = self._sub_module("searcher")

        # 如果Searcher为空，直接使用调用器返回
        if searcher is None:
            return caller.single_call(query, True)

        content = """
[人设]
你是一个查询关键词提取优化机器人
[任务]
1. 提取查询中的关键词集
2. 使用同义词，扩展关键词集，越重要的关键词扩展越多
[格式]
输入: 请问一下中大在2024年发生了什么?
输出: 中山大学,校史,2024年,学校历史,二零二四年

输入: %s
输出: 
        """

        # 1.预处理问题,得到关键词
        p_query = caller.single_call(content % query, False)

        # content = (
        #     "你现在的任务是找出问题的关键词，注意:提取的关键词中需要将“中大”更名为“中山大学”，下面是一个示例:\n"
        #     "Q:请问一下中大在2024年发生了什么? A:中山大学,校史,2024年 \n"
        #     "现在的问题是" + query
        # )

        # # 1.预处理问题,得到关键词
        # p_query = caller.single_call(content, False)

        # print("--预处理后得到的关键词为:", p_query)

        # 2.使用es查询得到相似问题
        sim_query = searcher.search(p_query, 3)
        # print(sim_query)

        # prefix_query = (
        #     "question:哈哈哈哈\n"
        #     + "data:参考资料1:中山大学图书馆是国际图书馆协会联合会(IFLA)会员机构,环太平洋学术图书馆联盟(PRRLA)成员馆,"
        #     + "教育部部级科技查新工作站和首批国家知识产权信息服务中心\n"
        #     + "answer:很高兴看到你这么开心\n"
        #     + "question:体育设施完善吗？\n"
        #     + "data:参考资料1:中山大学校徽为圆形图案,校徽上部自左而右环绕中文校名标准全称,下部自左而右环绕英文校名标准全称,中间为海棠式洞窗图案。\n"
        #     + "answer:抱歉,我暂时不能回答这个问题哟。\n"
        #     + "question:介绍一下中法核:\n"
        #     + "data:参考资料1:中山大学与法国民用核能工程师教学联盟合作建立了中法核工程与技术学院。"
        #     + "2016年,学院获得法国工程师职衔委员会(CTI)国际认证和欧洲工程教育认证(EUR-ACE),标志着学院办学水平已经达到了法国及欧洲的精英教育水平。"
        #     + "2016年6月,学院荣获中法两国政府联合颁发的“中法大学合作优秀项目”奖项。\n"
        #     + "     参考资料2:校训词为“博学 审问 慎思 明辨 笃行”。\n"
        #     + "answer:中山大学中法核工程与技术学院是中山大学与法国合作的精英学院,提供核工程与技术专业。"
        #     + "2016年6月,学院荣获中法两国政府联合颁发的“中法大学合作优秀项目”奖项。\n\n"
        # )
        demonstrate_prompt = """
[示范]
一
用户问题
国际学生政策是怎样的？
参考资料
参考资料1:国际学生政策:详情可见中山大学留学生办公室官网
回答
国际学生政策，官网有最权威的信息哦！快去中山大学留学生办公室官网看看吧，你会有新发现的！

二
用户问题
可以介绍一下你自己嘛？
参考资料
参考资料1:中山大学校校歌歌词:白云山高,珠江水长,吾校矗立,蔚为国光,中山手创
回答
嗨！我是中小大，中大软件工程学院的大二学生，也是校史介绍官。我超爱写代码和阅读历史书籍！

三
用户问题
为什么皮卡丘喜欢放电
参考资料
参考资料1:中山大学的微电子科学与技术学院本科招生专业:微电子科学与工程
参考资料2:中山大学的集成电路学院本科招生专业:微电子科学与工程
回答
很抱歉，我只是一个校史介绍官，不能回答关于皮卡丘的问题哦~
"""

        final_query = demonstrate_prompt + "\n[用户问题]\n" + query + "\n\n[参考资料]"

        for _id, _query in enumerate(sim_query):
            final_query += "\n参考资料" + str(_id + 1) + ":" + _query
        # print(final_query)
        return caller.single_call(final_query, True)
