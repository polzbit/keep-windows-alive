from KeepAlive.core.db._model import DBModel
import pandas as pd
from datetime import datetime

class Tasks(DBModel):
    def __init__(self):
        model = {
            'name': 'tasks', 
            'keys':[
                ('id','INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL'), 
                ('date', 'TIMESTAMP'),
                ('title', 'VARCHAR(140)'),
                ('duration', 'INTEGER'),
                ('project_id', 'INTEGER')
                ]
            }
        super().__init__(model) 
    
    def getTasks(self, projectId, date: pd.Timestamp = pd.to_datetime(datetime.now()), byDay = False):
        monthText = f'0{date.month}'
        dayText = f'0{date.day}'
        if(date.month > 9):
            monthText = f'{date.month}'
        if(date.day > 9):
            dayText = f'{date.day}'
        keys = ['id', 'date', 'title', 'duration']
        where = [('project_id', projectId), ("strftime('%m', date)", monthText), ("strftime('%Y', date)", f"{date.year}")]
        if byDay:
            where.append(("strftime('%d', start)", dayText))
        return self.get(keys=keys, where=where)
    
    def updateTask(self, projectId, taskId:int|None, date: pd.Timestamp, title:str, duration:str):
        if(not taskId):
            keys = [('title', title), ('date', date), ('duration', duration), ('project_id', projectId)]
            self.create(keys=keys)
        else:
            keys = [('title', title), ('date', date), ('duration', duration)]
            where = [('id', taskId)]
            self.update(keys=keys, where=where)