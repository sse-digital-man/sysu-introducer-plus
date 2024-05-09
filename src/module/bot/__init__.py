from .kind import CallerKind
from ..interface import BasicModule
from .searcher.es import EsSearcher
from .caller.gpt import GptCaller


BOT = "bot"
BASE_PATH = f"module.{BOT}"

class BasicBot(BasicModule):
    system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def __init__(self):
        super().__init__(BOT)
        self._es = EsSearcher()
        self._gpt = GptCaller()

    def _load_config(self):
        self._gpt._load_config()
        pass

    def talk(self, query: str) -> str:
        content= "你现在的任务是找出问题的关键词，下面是一个示例:\n Q:请问一下中山大学在2024年发生了什么? A:中山大学,校史,2024年 \n 现在的问题是" + query
        # 1.预处理问题,得到关键词
        p_query = self._gpt.single_call(content , False)
        # print("--预处理后得到的关键词为:", p_query)
        
        # 2.使用es查询得到相似问题
        sim_query = self._es.search(p_query, 3)
        # print(sim_query)

        # 3.生成最后的交互结果
        final_query = "请回答问题:" + query + "下面是参考资料,如果参考资料与“中山大学”无关,请礼貌回答:\n"
        # 3.生成最后的交互结果
        for _id, _query in enumerate(sim_query):
            final_query += "参考资料"+ str(_id+1) +":"+ _query+"\n"
        print(final_query)
        return self._gpt.single_call(final_query , True)
    

    def caller_kind(self) -> CallerKind:
        return self._caller.kind