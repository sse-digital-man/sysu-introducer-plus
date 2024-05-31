import json
from typing import Dict, List, Any

import yaml


UTF_8 = "utf-8"


def load_yaml(path: str) -> Dict:
    with open(path, "r", encoding=UTF_8) as f:
        return yaml.load(f, yaml.FullLoader)


def load_json(path: str) -> Dict | List:
    with open(path, "r", encoding=UTF_8) as f:
        return json.load(f)


def save_json(path: str, content: Dict):
    with open(path, "w", encoding=UTF_8) as f:
        json.dump(content, f, indent=4)


def load_lines(path: str) -> List[str]:
    try:
        with open(path, "r", encoding=UTF_8) as f:
            messages = f.readlines(-1)

            # 清除换行符
            for i, message in enumerate(messages):
                messages[i] = message.strip()

            return messages
    except BaseException:
        return []


def join_path(*args: str):
    return "/".join(args)


def dump_json(o: Any, indent: int = 0) -> str:
    return json.dumps(o, ensure_ascii=False, indent=indent)
