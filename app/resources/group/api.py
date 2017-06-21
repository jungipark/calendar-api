# coding=utf-8
from flask import Blueprint, request, current_app
from flask import g

from ..decorators import token_required
from ..exception_handle import exception_handle
from ..utils import model_to_list
from ..vaildation_check import check_required
from ...commons.response_data import ResponseData, HttpStatusCode
from ...commons.utils import string_to_datetime, get_current_time
from ...model import db, Event, Group

group_api = Blueprint("group_api", __name__, url_prefix='/api/v1/group')


@exception_handle
@group_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def default():
    """
    그룹 추가, 수정, 삭제
    :return:
    """
    # 그룹 추가
    if request.method == 'POST':
        req = request.get_json()
        if not check_required(required=['group_name'],
                              inspected_dict=req):
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        try:
            group = Group(creator_email=g.useremail,
                          name=req['group_name'],
                          created=get_current_time())
            db.session.add(group)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.debug(e)
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json
        return ResponseData(code=HttpStatusCode.SUCCESS).json

    # 그룹명 수정
    elif request.method == 'PUT':
        req = request.get_json()
        if not check_required(required=['group_id', 'group_name'],
                              inspected_dict=req):
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json

        try:
            group = db.session.query(Group).filter(Group.id == req['group_id']).first()

            if group is not None:
                if group.creator_email != g.useremail:
                    return ResponseData(code=HttpStatusCode.UNAUTHORIZED_REQUEST).json
                group.name = req['group_name']
                group.updated = get_current_time()
                db.session.commit()
            else:
                return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json

        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e, exc_info=True)
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json

        return ResponseData(code=HttpStatusCode.SUCCESS).json


    # 그룹 삭제
    elif request.method == 'DELETE':
        req = request.get_json()
        if not check_required(required=['group_id'],
                              inspected_dict=req):
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        group = Group.query.filter_by(id=int(req['group_id'])).first()
        if group is None:
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        group_event = Event.query.filter_by(group=int(req['group_id'])).all()
        if group_event is not None:
            Event.query.filter_by(group=int(req['group_id'])).delete()
        db.session.delete(group)
        db.session.commit()
        return ResponseData(code=HttpStatusCode.SUCCESS).json

    # 내가 생성한 그룹 조회
    elif request.method == 'GET':
        groups = db.session.query(Group).filter(Group.creator_email == g.useremail).all()
        res_list = model_to_list(groups)
        return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@group_api.route('/list', methods=['GET'])
@token_required
def group_list():
    """
    전체 그룹 조회(다른 유저가 등록한 그룹도 조회 가능)
    :return:
    """
    groups = db.session.query(Group).filter().all()
    res_list = model_to_list(groups)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@group_api.route('/event', methods=['POST'])
@token_required
def event():
    """
    특정 그룹에 일정 등록
    :return:
    """
    req = request.get_json()
    if not check_required(required=['subject', 'sdate', 'edate', 'group_id'],
                          inspected_dict=req):
        return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
    group = db.session.query(Group).filter(Group.id == int(req['group_id'])).first()
    if group is None:
        return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
    try:
        event = Event(email=g.useremail,
                      subject=req['subject'],
                      sdate=string_to_datetime(req['sdate']),
                      edate=string_to_datetime(req['edate']),
                      group=req['group_id'],
                      created=get_current_time())
        db.session.add(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(e, exc_info=True)
        return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json

    return ResponseData(code=HttpStatusCode.SUCCESS).json
