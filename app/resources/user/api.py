# coding=utf-8
from flask import Blueprint, request, g

from ..decorators import token_required
from ..exception_handle import exception_handle
from ..vaildation_check import check_required
from ...commons.jwt_token import create_jwt_token
from ...commons.response_data import ResponseData, HttpStatusCode
from ...model import db, User, Group

user_api = Blueprint("user_api", __name__, url_prefix='/api/v1/user')


@exception_handle
@user_api.route('/', methods=['POST'])
def default():
    """
    유저 생성 및 토큰 발급
    :return: 
    """
    req = request.get_json()
    if not check_required(required=['useremail'],
                          inspected_dict=req):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    user = User.query.filter_by(email=req['useremail']).first()
    if user is None:
        token = create_jwt_token(req['useremail'])
        user = User(email=req['useremail'], token=token)
        db.session.add(user)
        db.session.commit()
    else:
        return ResponseData(code=HttpStatusCode.USER_ID_EXIST).json
    return ResponseData(code=HttpStatusCode.SUCCESS, data={'token': token}).json


@exception_handle
@user_api.route('/calendar/group', methods=['POST'])
@token_required
def calendar_group():
    """
    자신의 캘린더에 표시할 그룹을 선택
    req = {'selected_group': '1,2,3,5'}
    :return: 
    """
    req = request.get_json()
    if not check_required(required=['selected_group'],
                          inspected_dict=req):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    user = db.session.query(User).filter(User.email == g.useremail).first()

    if str(req['selected_group']) == "0":
        user.selected_calendar_group = None
        db.session.commit()
        return ResponseData(code=HttpStatusCode.SUCCESS).json

    selected_group_list = []
    if str(req['selected_group'].find(',')) == "1":
        selected_group_list = map(int, str(req['selected_group']).split(','))
    elif str(req['selected_group'].find(',')) == "-1":
        selected_group_list = map(int, str(req['selected_group']))

    groups = db.session.query(Group).filter().all()
    group_list = []
    [group_list.append(group.id) for group in groups]
    intersected_group = set(group_list).intersection(set(selected_group_list))
    if intersected_group != set(selected_group_list):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    user.selected_calendar_group = req['selected_group']
    db.session.commit()
    return ResponseData(code=HttpStatusCode.SUCCESS).json
