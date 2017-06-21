# coding=utf-8
from ..commons.response_data import ResponseData, HttpStatusCode
from ..model import db, User


def model_to_list(data_list):
    res_list = []
    for data in data_list:
        res_list.append(data.tojson())
    return res_list


def selected_calendar_group(useremail):
    user = db.session.query(User).filter(User.email == useremail).first()
    user_select_group_list = []
    if user is None:
        return ResponseData(code=HttpStatusCode.BAD_REQUEST).json

    if user.selected_calendar_group is not None:
        if user.selected_calendar_group.find(',') == 1:
            user_select_group_list = user.selected_calendar_group.split(',')
        else:
            user_select_group_list.append(int(user.selected_calendar_group))
    return user_select_group_list
