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
        # 返回 模块的所有配置信息
        if kind is None:
            return Config._data[name]
        else:
            return Config._data[name][kind]
        
    def update(self, name: str, kind: str, content: Dict, save: bool=False):
        origin = self.get(name, kind).copy()

        for (key, value) in content.items():
            origin_t, new_t = type(origin[key]), type(value)
            
            # 验证模块类型是否匹配
            if origin_t != new_t:
                raise TypeError(
                    f"the filed '{key}' doesn't match ('{origin_t}') excepted, '{new_t}' given", \
                    key, origin_t, new_t
                )
            
            origin[key] = value
        
        Config._data[name][kind] = origin

        if save:
            save_json(CONFIG_PATH, Config._data)

    @staticmethod
    def reload():
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
            Config._data = json.load(f)

config = Config()