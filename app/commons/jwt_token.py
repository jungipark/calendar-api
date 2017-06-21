# coding=utf-8
from jose import jwt


def create_jwt_token(useremail):
    """
    JWT 토큰을 생성한다.
    :param useremail: 사용자 email
    :return: JWT 토큰
    """

    jwt_claim_set = {
        'iss': 'JUNGIPARK',  # 토큰 발행자
        'aud': 'CALENDAR_API',  # 토큰 사용자
        'useremail': useremail
    }
    token = jwt.encode(jwt_claim_set, 'secret_key_2017', algorithm='HS256')
    return token


def parse_jwt_token(token):
    """
    JWT 토큰 파싱
    :param token: JWT 토큰 문자열
    :return: JWT 토큰 데이터
    """
    try:

        result = jwt.decode(token, 'secret_key_2017', algorithms=['HS256'], subject="JUNGIPARK",
                            audience='CALENDAR_API')
        result['useremail'] = result['useremail']
        return result
    except Exception as e:
        raise e
