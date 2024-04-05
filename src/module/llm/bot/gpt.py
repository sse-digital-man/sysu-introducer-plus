import openai
from typing import List
import numpy as np
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
)

from src.data import data_collection

from .base import BasicBot
from utils.config import config

# Migration Guide: https://github.com/openai/openai-python/discussions/742


class GPTBot(BasicBot):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__()
        api_key, url = GPTBot.__get_config()

        self.client = openai.OpenAI(api_key=api_key, base_url=url, timeout=5)

    def _load_config(self):
        api_key, url = GPTBot.__get_config()

        self.client.api_key = api_key
        self.client.base_url = url

        print(self.client.api_key)
        print(self.client.base_url)

    @staticmethod
    def __get_config():
        info = config.get_system_module("llm", "gpt")
        return info["apiKey"], info["url"]

    def _single_call(self, query: str) -> str:
        new_question_embedding = data_collection.model[query]

        closest_text = None
        closest_distance = float("inf")
        for text in data_collection.r.hkeys("knowledge_base_embeddings"):
            text_embedding = np.frombuffer(
                data_collection.r.hget("knowledge_base_embeddings", text),
                dtype=np.float32,
            )
            distance = np.linalg.norm(new_question_embedding - text_embedding)
            if distance < closest_distance:
                closest_distance = distance
                closest_text = text

        messages = [
            {"role": "system", "content": BasicBot.system_prompt},
            {
                "role": "user",
                # "content": query
                "content": closest_text.decode("utf-8"),
            },
        ]

        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages,
        )

        return response.choices[0].message.content
