from calendar import monthrange, month_name
from datetime import datetime
import pandas as pd

def get_month_list():
    def filterEmpty(variable):
        return variable != ''
    return list(filter(filterEmpty, list(month_name)))

def get_current_days(current_date = datetime.now()):
    date = pd.to_datetime(current_date)
    return (current_date.year, current_date.month, date.month_name(), monthrange(current_date.year, current_date.month)[1])

def is_weekday(day, timeSheet):
    date = pd.to_datetime(day, dayfirst=True)
    weekday = date.weekday()
    name = date.day_name()
    currentRecord = None
    for i in range(len(timeSheet)):
        start = pd.to_datetime(timeSheet[i][1], dayfirst=False)
        if timeSheet[i][2] != '':
            end = pd.to_datetime(timeSheet[i][2], dayfirst=False).strftime('%X')
        else:
            end = ''
        if start.date() == date.date():
            currentRecord = (timeSheet[i][0], start.strftime('%X'), end, timeSheet[i][3])
            break
    return (name, weekday < 4 or weekday > 5, currentRecord)
