from typing import Any
from werkzeug.wrappers import Response
from flask import jsonify

class Result:
    @staticmethod
    def create(info: dict=None, code: int=0):
        return {
            "info": info,
            "code": code
        }

class ResultResponse(Response):
    default_mimetype = "application/json"

    @classmethod
    def force_type(cls, response: Response, environ: dict[str, Any] | None = None) -> Response:
        if isinstance(response, dict):
            response(jsonify(response))

        return super(ResultResponse, cls).force_type(response, environ)