import openai
from typing import List

from .base import BasicBot
from utils.config import LLMConfig

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class GPTBot(BasicBot):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__()

        self.client = openai.OpenAI(
            api_key=LLMConfig.GPT_API_KEY,
            base_url=LLMConfig.GPT_BASE_URL
        )
    
    # 
    def _single_call(self, query: str) -> str:
        messages = [
            {
                "role": "system",
                "content": BasicBot.system_prompt
            }, {
                "role": "user",
                "content": query
            }
        ]

        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content