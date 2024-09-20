from calendar import monthrange, month_name
from datetime import datetime
import pandas as pd

def get_month_list():
    def filterEmpty(variable):
        return variable != ''
    return list(filter(filterEmpty, list(month_name)))

def get_current_days(current_date = datetime.now()):
    date = pd.to_datetime(current_date)
    return (current_date.year, current_date.month, date.month_name(), monthrange(current_date.year, current_date.month)[1], date.day)

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

def get_runtime_seconds(runtime):
    runtime_dur = runtime.split(':')
    runtime_hours = int(runtime_dur[0]) * 3600
    runtime_minutes = int(runtime_dur[1]) * 60
    total_seconds = runtime_hours + runtime_minutes + int(runtime_dur[2])
    return total_seconds

def get_runtime_text(runtime_seconds):
    sec = runtime_seconds
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)
