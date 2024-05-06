import json
from typing import Dict

from .file import save_json

CONFIG_PATH = 'config.json'

class Config:
    _data = None

    def __init__(self):
        if Config._data == None:
            Config.reload()

        
    # def get(self, *keys):
    #     result = Config._data
    #     for key in keys:
    #         result = result[key]
    #         if result is None:
    #             return None

    #     return result
    
    def get(self, name: str, kind: str=None) -> Dict:
        print(self._data[name])

        if kind is None:
            return Config._data[name]
        else:
            return Config._data[name][kind]
        
    def update(self, content: Dict, name: str, kind: str=None, save: bool=False):
        if kind is None:
            Config._data[name] = content
        else:
            Config._data[name][kind] = content

        if save:
            save_json(CONFIG_PATH, Config._data)

    @staticmethod
    def reload():
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
            Config._data = json.load(f)

config = Config()