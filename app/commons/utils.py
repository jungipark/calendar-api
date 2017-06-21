import datetime
from datetime import datetime as dt
import pytz


def string_to_datetime(string_datetime):
    return dt.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")


def string_to_date(string_date):
    return dt.strptime(string_date, '%Y-%m-%d').date()


def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))


