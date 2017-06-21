# coding=utf-8

class EnumMeta(type):
    """
    class 변수에 값에 대한 변수이름반환을 위한 EnumMeta 클래스
    """

    def __getitem__(self, item):

        if item is None:
            return None
        var = None

        for k, v in vars(self).iteritems():
            if v == item:
                var = k
                break
        return var


class HttpStatusCode(object):
    __metaclass__ = EnumMeta

    SUCCESS = 20000  # 기본
    USER_ID_EXIST = 20010
    USER_BIRTHDAY_EXIST = 20011

    BAD_REQUEST = 40000  # 기본
    INVALID_PARAMETER = 40001

    UNAUTHORIZED = 40100  # 기본
    MISSING_HEADER = 40101
    INVALID_TOKEN = 40102
    UNAUTHORIZED_REQUEST = 40103

    FORBIDDEN = 40300  # 기본

    NOT_FOUND = 40400  # 기본

    INTERNAL_SERVER_ERROR = 50000  # 기본


class ResponseData(object):
    meta = None
    data = None

    def __init__(self, code=200, success_msg_code=None, data=None):
        self.meta = Meta(code=code, success_msg_code=success_msg_code)
        self.data = data
        # self.data = data

    def to_dict(self):
        result = dict()
        result["meta"] = self.meta.__dict__
        if self.data is not None:
            result["data"] = self.data
        return result

    @property
    def json(self):
        from flask import jsonify
        http_status_code = int(str(self.meta.code)[:3])
        return jsonify(self.to_dict()), http_status_code


class Meta(object):
    code = None
    message = None
    msg = None

    def __init__(self, code=HttpStatusCode.SUCCESS, success_msg_code=None):
        self.code = code
        self.message = HttpStatusCode[self.code]
