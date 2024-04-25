from enum import Enum


class CallerKind(Enum):
    GPT = "gpt"
    Virtual = "virtual"

class SearcherKind(Enum):
    NULL = "null"