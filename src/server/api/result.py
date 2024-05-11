from typing import Any, Tuple, Dict
from enum import Enum

from werkzeug.wrappers import Response
from flask import jsonify

class ErrorCode(Enum):
    # Error = (0, "错误", 500)
    Ok = (1, "成功", 200)

    KeyDataMissing = (101, "缺少关键数据", 400)

    # 模块相关错误
    ModuleNotFound =( 201, "模块不存在", 404)
    ModuleUncontrollable = (202, "模块不可控", 400)
    ModuleStatusNotSupported = (203, "模块状态不支持", 400)
    ModuleConfigEmpty = (204, "模块无配置信息", 200)
    ModuleConfigItemNotFound = (205, "模块配置信息条目不存在", 404),
    ModuleConfigItemTypeUnmatched = (206, "模块信息条目类型不匹配", 400)
    ModuleKindNotFound = (207, "模块实现类型不存在", 404)

class Result:
    @staticmethod
    def create(data: dict=None, code: ErrorCode=ErrorCode.Ok) ->Tuple[Dict, int]:
        """返回相应数据和状态码，默认返回成功

        Args:
            data (dict, optional): 相应数据 Defaults to None.
            code (ErrorCode, optional): 状态码 Defaults to ErrorCode.Ok.

        Returns:
            Tuple[Dict, int]:  Flask返回的格式
        """

        item = code.value

        return {
            "data": data,
            "code": item[0],
            "message": item[1]
        }, item[2]

class ResultResponse(Response):
    default_mimetype = "text/html; charset=utf-8"

    @classmethod
    def force_type(cls, response: Response, environ: dict[str, Any] | None = None) -> Response:
        if isinstance(response, dict):
            response = jsonify(response)
            response.headers['Content-Type'] = "application/json"

        return super(ResultResponse, cls).force_type(response, environ)