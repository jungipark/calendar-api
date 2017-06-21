# coding=utf-8

def check_required(required, inspected_dict):
    """
    필수 데이터 체크
    :param required: 체크해야할 항목
    :param inspected_dict: 체크할 dict
    :return: 체크해야할 항목이 dict에 다 있으면 true, 아니면 false
    """

    if isinstance(required, list) and isinstance(inspected_dict, dict):
        intersected = set(required).intersection(set(inspected_dict.keys()))
        if len(intersected) == len(required):
            return True
        else:
            return False


def check_required_get(required, request):
    """
    필수 데이터 체크
    :param required: 체크해야할 항목
    :param requset: 체크할 request
    :return: 체크해야할 항목이 다 있으면 true, 아니면 false
    """
    for r in required:
        if request.args.get(r) is None:
            return False
    return True
