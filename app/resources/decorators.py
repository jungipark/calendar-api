# coding=utf-8

from functools import wraps

from flask import g
from flask import request
from jose import JWTError

from app.commons.response_data import ResponseData, HttpStatusCode


def token_required(func):
    """
    로그인 이후, 전달되는 TOKEN 에 대한 확인
    """

    @wraps(func)
    def new_func(*args, **kwargs):
        access_token = None
        for header, value in request.headers.items():
            if header.upper() == "X-CALENDAR-ACCESS-TOKEN":
                access_token = value
        g.access_token = access_token
        if access_token:
            from ..commons.jwt_token import parse_jwt_token
            try:
                jwt_data = parse_jwt_token(token=access_token)
            except JWTError:
                return ResponseData(code=HttpStatusCode.INVALID_TOKEN).json
            from flask import current_app
            current_app.logger.debug(jwt_data)
            if jwt_data and 'useremail' in jwt_data:
                g.useremail = jwt_data['useremail']
                result = func(*args, **kwargs)
            else:
                result = ResponseData(code=HttpStatusCode.INVALID_TOKEN).json
        else:
            result = ResponseData(code=HttpStatusCode.MISSING_HEADER).json
        return result

    return new_func
