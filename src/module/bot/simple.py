from typing import Dict

from . import RagBot


class SimpleBot(RagBot):
    def load_config(self):
        pass

    @RagBot._handle_log
    def retrieve_sim_k(self, query: str, k: int) -> Dict[str, str]:
        caller = self._sub_module("caller")
        searcher = self._sub_module("searcher")

        # 如果Searcher为空，直接返回空字典
        if searcher is None:
            return {}

        # 1. 预处理问题,提取关键词
        content = \
"""
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

        p_query = caller.single_call(content % query, False)

        # 2. 使用es检索得到相似问题
        retrieve_res = searcher.search_with_label(p_query, 3)
        # print(retrieve_res)

        return retrieve_res
    
        # content = (
        #     "你现在的任务是找出问题的关键词，注意:提取的关键词中需要将“中大”更名为“中山大学”，下面是一个示例:\n"
        #     "Q:请问一下中大在2024年发生了什么? A:中山大学,校史,2024年 \n"
        #     "现在的问题是" + query
        # )

        # # 1.预处理问题,得到关键词
        # p_query = caller.single_call(content, False)

        # print("--预处理后得到的关键词为:", p_query)

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