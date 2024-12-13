from json import dumps
from urllib import response

from flask import jsonify
from werkzeug.wrappers import Response

import app.common.status as status


def make_response(code: int, msg: str, data=None) -> Response:
    payload = {"code": code, "msg": msg, "data": data}
    response = jsonify(payload)

    # 加了下面这一行会触发 axios 的 onError， 不加则触发 onBackendFail
    # response.status_code = code
    return response


def success(data=None, msg="请求成功") -> Response:
    return make_response(code=status.HTTP_200_OK, msg=msg, data=data)


def failed(code, msg=None, data=None) -> Response:
    return make_response(code=code, msg=msg, data=data)
