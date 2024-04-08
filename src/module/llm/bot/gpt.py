import openai
from typing import List

from .base import BasicBot
from .esbot import ESBot
from ..bot_kind import BotKind
from utils.config import config

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class GPTBot(ESBot):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__(BotKind.GPT)
        api_key, url = GPTBot.__get_config()

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=url,
            timeout=5
        )

    def _load_config(self):
        api_key, url = GPTBot.__get_config()

        self.client.api_key = api_key
        self.client.base_url = url

        print(self.client.api_key)
        print(self.client.base_url)

    @staticmethod
    def __get_config():
        info = config.get_system_module("llm", "gpt")
        return info['apiKey'], info['url']

    def _single_call(self, query: str, use_system_prompt: bool) -> str:
        messages = []
        if use_system_prompt:
            messages.append({
                "role": "system",
                "content": BasicBot.system_prompt
            })
        messages.append({
            "role": "user",
            "content": query
        })

        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content
    
    # def talk(self, query: str) -> str:
    #     return super().talk(query)