import openai

from .interface import CallerInterface

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class GptCaller(CallerInterface):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__()

        self.__client = openai.OpenAI(
            api_key="",
            base_url=None,
            timeout=5
        )

    def _load_config(self):
        info = self._read_config()

        self.__client.api_key = info['apiKey']
        self.__client.base_url = info['url']

        # print(self.client.api_key)
        # print(self.client.base_url)

    def single_call(self, query: str, with_system_prompt: bool=True) -> str:
        messages = []

        if with_system_prompt:
            messages.append({
                "role": "system",
                "content": self._system_prompt
            })

        messages.append({
            "role": "user",
            "content": query
        })

        response = self.__client.chat.completions.create(
            model=self.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content