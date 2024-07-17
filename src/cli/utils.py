from typing import List, Callable
from tabulate import tabulate


TABLE_STYLE = "github"

TranslateFunc = Callable[[dict, str], str]


def generate_table(
    data: List[dict], headers: List[str] = None, translate_cell: TranslateFunc = None
) -> str:

    def default_translate_func(info, header):
        return info[header]

    if len(data) == 0:
        return ""

    keys = data[0].keys()
    if headers is None:
        headers = keys
    else:
        # 对输入的头部进行校验
        for header in headers:
            if header not in keys:
                raise KeyError()

    if translate_cell is None:
        translate_cell = default_translate_func

    rows = [[translate_cell(info, header) for header in headers] for info in data]

    return "\n" + tabulate(rows, headers, tablefmt=TABLE_STYLE)
