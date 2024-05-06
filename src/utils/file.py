import json

from typing import Dict, List

def load_json(path: str) -> Dict | List:
    with open(path, 'r', encoding='UTF-8') as f:
        return json.load(f)