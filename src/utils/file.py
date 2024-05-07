import json

from typing import Dict, List

def load_json(path: str) -> Dict | List:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_json(path: str, content: Dict):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(content, f, indent=4)