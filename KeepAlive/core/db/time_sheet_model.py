from KeepAlive.core.db._model import DBModel
import pandas as pd
from datetime import datetime

class TimeSheet(DBModel):
    def __init__(self):
        model = {
            'name': 'timeSheet', 
            'keys':[
                ('id','INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL'), 
                ('start', 'TIMESTAMP NOT NULL'),
                ('end', 'TIMESTAMP'),
                ('duration', 'VARCHAR(40)'),
                ('project_id', 'INTEGER')
                ]
            }
        super().__init__(model) 
    
    def getTimeSheet(self, projectId, date: pd.Timestamp = pd.to_datetime(datetime.now()), byDay = False):
        monthText = f'0{date.month}'
        dayText = f'0{date.day}'
        if(date.month > 9):
            monthText = f'{date.month}'
        if(date.day > 9):
            dayText = f'{date.day}'
        keys = ['id', 'start', 'end', 'duration']
        where = [('project_id', projectId), ("strftime('%m', start)", monthText), ("strftime('%Y', start)", f"{date.year}")]
        if byDay:
            where.append(("strftime('%d', start)", dayText))
        return self.get(keys=keys, where=where)
    
    def createTimestamp(self, projectId, duration, end):
        date = pd.to_datetime(datetime.now())
        data = self.getTimeSheet(projectId, date, True)
        if(not end and not len(data)):
            keys = [('start', date), ('project_id', projectId)]
            self.create(keys=keys)
        elif end and len(data):
            keys = [('end', date), ('duration', duration)]
            where = [('id', data[0][0])]
            self.update(keys=keys, where=where)

    def updateTimestamp(self, date, projectId, start, end, duration):
        currentDate = pd.to_datetime(date, dayfirst=True)
        startDate = pd.to_datetime(f"{currentDate.year}/{currentDate.month}/{currentDate.day} {start}")
        endDate = pd.to_datetime(f"{currentDate.year}/{currentDate.month}/{currentDate.day} {end}")
        data = self.getTimeSheet(projectId, startDate, True)
        if(not len(data)):
            keys = [('start', startDate), ('end', endDate), ('duration', duration), ('project_id', projectId)]
            self.create(keys=keys)
        else:
            keys = [('start', startDate), ('end', endDate), ('duration', duration)]
            where = [('id', data[0][0])]
            self.update(keys=keys, where=where)