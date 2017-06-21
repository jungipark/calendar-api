# coding=utf-8
import datetime

from flask import Blueprint, request, current_app
from flask import g
from sqlalchemy import extract, func, or_, and_

from app.commons.utils import string_to_datetime, string_to_date, get_current_time
from ..decorators import token_required
from ..exception_handle import exception_handle
from ..utils import model_to_list, selected_calendar_group
from ..vaildation_check import check_required, check_required_get
from ...commons.response_data import ResponseData, HttpStatusCode
from ...model import db, Event

calendar_api = Blueprint("calendar_api", __name__, url_prefix='/api/v1/calendar')


@exception_handle
@calendar_api.route('/', methods=['GET'])
@token_required
def default():
    """
    기본적으로 월별 캘린더는 이번달 일정 전체를 조회
    """
    user_select_group_list = selected_calendar_group(g.useremail)
    d = datetime.date.today()
    events = db.session.query(Event). \
        filter(Event.email == g.useremail). \
        filter(or_(Event.group.in_(user_select_group_list), Event.group == None)). \
        filter(extract('month', Event.sdate) == d.month).all()
    res_list = model_to_list(events)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@calendar_api.route('/month', methods=['GET'])
@token_required
def month():
    """
    다른달로 이동 
    월별 일정 조회 
    """
    user_select_group_list = selected_calendar_group(g.useremail)
    req = {}

    if not check_required_get(required=['year_month'], request=request):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    req['year_month'] = request.args.get('year_month')
    year_month = req['year_month'].split('-')
    events = db.session.query(Event). \
        filter(Event.email == g.useremail). \
        filter(or_(Event.group.in_(user_select_group_list), Event.group == None)). \
        filter(extract('year', Event.sdate) == int(year_month[0])). \
        filter(extract('month', Event.sdate) == int(year_month[1])).all()
    res_list = model_to_list(events)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@calendar_api.route('/event', methods=['POST', 'PUT', 'DELETE'])
@token_required
def event():
    """
    일정 등록, 수정, 삭제 조회
    """
    # 일정 등록
    if request.method == "POST":
        try:
            req = request.get_json()
            if not check_required(required=['sdate', 'edate', 'subject'],
                                  inspected_dict=req):
                return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
            event = Event(email=g.useremail,
                          sdate=string_to_datetime(req["sdate"]),
                          edate=string_to_datetime(req["edate"]),
                          subject=req["subject"],
                          created=get_current_time())
            db.session.add(event)
            db.session.commit()
        except ValueError:
            db.session.rollback()
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        except Exception as e:
            db.session.rollback()
            current_app.logger.debug(e)
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json

        return ResponseData(code=HttpStatusCode.SUCCESS).json


    # 일정 수정
    elif request.method == "PUT":
        req = request.get_json()
        if not check_required(required=['event_id', 'sdate', 'edate', 'subject'],
                              inspected_dict=req):
            return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json
        try:
            event = db.session.query(Event).filter(Event.id==req['event_id']).first()
            if event is None:
                return ResponseData(code=HttpStatusCode.INVALID_PARAMETER).json

            if event.email != g.useremail:
                return ResponseData(code=HttpStatusCode.UNAUTHORIZED_REQUEST).json

            event.updated = get_current_time()
            event.sdate = string_to_datetime(req['sdate'])
            event.edate = string_to_datetime(req['edate'])
            event.subject = req['subject']
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.debug(e)
            return ResponseData(code=HttpStatusCode.INTERNAL_SERVER_ERROR).json

        return ResponseData(code=HttpStatusCode.SUCCESS).json


    # 일정 삭제
    elif request.method == "DELETE":
        req = request.get_json()
        if not check_required(required=['event_id'],
                              inspected_dict=req):
            return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
        try:
            event = db.session.query(Event).filter(Event.id == req['event_id']).first()
            if event is None:
                return ResponseData(HttpStatusCode.INVALID_PARAMETER).json

            if event.email != g.useremail:
                return ResponseData(code=HttpStatusCode.UNAUTHORIZED_REQUEST).json

            db.session.delete(event)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.debug(e)
            return ResponseData(HttpStatusCode.INTERNAL_SERVER_ERROR).json
        return ResponseData(HttpStatusCode.SUCCESS).json


@exception_handle
@calendar_api.route('/today', methods=['GET'])
@token_required
def today():
    """
    캘린더 오늘 날짜 일정 조회
    """
    today = datetime.date.today()
    user_select_group_list = selected_calendar_group(g.useremail)
    events = db.session.query(Event). \
        filter(Event.email == g.useremail). \
        filter(or_(Event.group.in_(user_select_group_list), Event.group == None)). \
        filter(or_(func.Date(Event.sdate) == today, func.Date(Event.edate) == today)).all()
    res_list = model_to_list(events)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@calendar_api.route('/date', methods=['GET'])
@token_required
def date():
    """
    특정 날짜 일정 조회
    req = {'date': '2017-06-20'}
    :return: 
    """
    user_select_group_list = selected_calendar_group(g.useremail)
    req = {}

    if not check_required_get(required=['date'], request=request):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    req['date'] = request.args.get('date')

    date = string_to_date(req['date'])
    events = db.session.query(Event). \
        filter(Event.email == g.useremail). \
        filter(or_(Event.group.in_(user_select_group_list), Event.group == None)). \
        filter(or_(func.Date(Event.sdate) == date, func.Date(Event.edate) == date)).all()
    res_list = model_to_list(events)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@calendar_api.route('/search', methods=['GET'])
@token_required
def search():
    """
    일정 검색, 제목으로 검색
    :return: 
    """
    user_select_group_list = selected_calendar_group(g.useremail)
    req = {}
    if not check_required_get(required=['search_word'], request=request):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    req['search_word'] = request.args.get('search_word')
    events = db.session.query(Event). \
        filter(Event.email == g.useremail). \
        filter(or_(Event.group.in_(user_select_group_list), Event.group == None)). \
        filter(Event.subject.like("%" + req['search_word'] + "%")).all()

    res_list = model_to_list(events)
    return ResponseData(code=HttpStatusCode.SUCCESS, data=res_list).json


@exception_handle
@calendar_api.route('/birthday', methods=['POST'])
@token_required
def birthday():
    """
    캘린더에 생일 등록
    req = {'birthday': '2017-06-29'}
    :return: 
    """
    req = request.get_json()
    if not check_required(required=['birthday'],
                          inspected_dict=req):
        return ResponseData(HttpStatusCode.INVALID_PARAMETER).json
    req_birthday = string_to_date(req['birthday'])
    event = db.session.query(Event).filter(and_(Event.email == g.useremail, Event.birthday == 1)).first()
    if event is None:
        register_birthday = Event(email=g.useremail,
                                  subject=g.useremail + u" 생일",
                                  birthday=1,
                                  sdate=req_birthday,
                                  edate=req_birthday,
                                  created=get_current_time())
        db.session.add(register_birthday)
        db.session.commit()
    else:
        return ResponseData(HttpStatusCode.USER_BIRTHDAY_EXIST).json
    return ResponseData(HttpStatusCode.SUCCESS).json
