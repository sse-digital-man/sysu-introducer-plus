from ..interface import BasicModule


class BasicBot(BasicModule):
    system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def load_config(self):
        pass

    @BasicModule._handle_log
    def talk(self, query: str) -> str:
        return self._sub_module("caller").single_call(query, True)
