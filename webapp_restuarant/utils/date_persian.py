import jdatetime
import datetime as py_datetime


def date_fromgregorian(date):
    if type(date) == py_datetime.date:
        return jdatetime.date.fromgregorian(date=date, locale="fa_IR")
    elif type(date) == py_datetime.datetime:
        return jdatetime.datetime.fromgregorian(datetime=date, locale="fa_IR")
    else:
        return None
