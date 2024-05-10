from typing import Any
from werkzeug.wrappers import Response
from flask import jsonify

class Result:
    @staticmethod
    def create(data: dict=None, code: int=0):
        return {
            "data": data,
            "code": code
        }


class ResultResponse(Response):
    default_mimetype = "text/html; charset=utf-8"

    @classmethod
    def force_type(cls, response: Response, environ: dict[str, Any] | None = None) -> Response:
        if isinstance(response, dict):
            response = jsonify(response)
            response.headers['Content-Type'] = "application/json"

        return super(ResultResponse, cls).force_type(response, environ)