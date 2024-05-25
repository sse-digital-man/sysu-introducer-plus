from typing import Dict

from .file import save_json, load_json

CONFIG_PATH = "config.json"


class Config:

    def __init__(self):
        self._data: dict = load_json(CONFIG_PATH)

    # def get(self, *keys):
    #     result = Config._data
    #     for key in keys:
    #         result = result[key]
    #         if result is None:
    #             return None

    #     return result

    def get(self, name: str, kind: str = None) -> Dict:
        # 返回 模块的所有配置信息
        if kind is None:
            return self._data[name]
        else:
            return self._data[name][kind]

    def update(self, name: str, kind: str, content: Dict, save: bool = False):
        origin = self.get(name, kind).copy()

        for key, value in content.items():
            origin_t, new_t = type(origin[key]), type(value)

            # 验证模块类型是否匹配
            if origin_t != new_t:
                raise TypeError(
                    f"the filed '{key}' doesn't match ('{origin_t}') excepted, '{new_t}' given",
                    key,
                    origin_t,
                    new_t,
                )

            origin[key] = value

        self._data[name][kind] = origin

        if save:
            save_json(CONFIG_PATH, self._data)

    def reload(self):
        self._data = load_json(CONFIG_PATH)


CONFIG = Config()
