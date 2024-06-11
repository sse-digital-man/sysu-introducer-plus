from typing import Dict

from . import RagBot


class HydeBot(RagBot):
    def load_config(self):
        pass

    @RagBot._handle_log
    def retrieve_sim_k(self, query: str, k: int) -> Dict[str, str]:
        caller = self._sub_module("caller")
        searcher = self._sub_module("searcher")

        # 如果Searcher为空，直接返回空字典
        if searcher is None or searcher.kind != 'vector' or caller.kind != 'gpt':
            return {}

        # 1. 生成 hyde 假设性回答
        query = searcher.prompt_template.format(query=query)
        query += caller.single_call(query, False)

        # 2.使用 hyde 检索得到 top3 相似结果
        retrieve_res = searcher.search_with_label(query, k)

        return retrieve_res