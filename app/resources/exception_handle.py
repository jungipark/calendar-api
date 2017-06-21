# coding=utf-8
__author__ = 'jungi. park'

import functools

from flask import current_app

from ..commons.response_data import ResponseData, HttpStatusCode


def exception_handle(func):
    @functools.wraps(func)
    def newFunc(self, *args, **kwargs):
        result = None
        try:
            result = func(self, *args, **kwargs)
        except ValueError as ve:
            current_app.logger.exception(ve, exc_info=True)
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        except Exception as e:
            current_app.logger.exception(e, exc_info=True)
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json
        return result

    return newFunc
