from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pandas as pd
from datetime import datetime

class TimeSheetDb:
    def __init__(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName(".\\AppDb")
    
    def lastError(self):
        return self.con.lastError()
    
    def isConnectionOpen(self):
        return self.con.open()
    
    def clearTimeSheetTable(self):
        query = QSqlQuery()
        query.exec('delete from timeSheet')
    
    def getTimeSheet(self, date = pd.to_datetime(datetime.now()), byDay = False):
        query = QSqlQuery()
        monthText = f'0{date.month}'
        dayText = f'0{date.day}'
        if(date.month > 9):
            monthText = f'{date.month}'
        if(date.day > 9):
            dayText = f'{date.day}'
        if(byDay):
            query.exec(f"SELECT id, start, end, duration FROM timeSheet WHERE strftime('%m', start) = '{monthText}' AND strftime('%Y', start) = '{date.year}' AND strftime('%d', start) = '{dayText}'") 
        else:
            query.exec(f"SELECT id, start, end, duration FROM timeSheet WHERE strftime('%m', start) = '{monthText}' AND strftime('%Y', start) = '{date.year}'")
        id, start, end, duration = range(4)
        data = []
        while query.next():
            data.append((query.value(id), query.value(start), query.value(end), query.value(duration)))
        query.finish()
        return data
    
    def createTable(self):
        createTableQuery = QSqlQuery()
        createTableQuery.exec(
            """
            CREATE TABLE timeSheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                start TIMESTAMP NOT NULL,
                end TIMESTAMP,
                duration VARCHAR(40)
            )
            """
        )
    
    def createTimestamp(self,runtime, end):
        date = pd.to_datetime(datetime.now())
        query = QSqlQuery()
        data = self.getTimeSheet(date, True)
        if(not end and not len(data)):
            query.exec(
                f"""INSERT INTO timeSheet (start)
                VALUES ('{date}')"""
            )
        elif end and len(data):
            runtime_dur = runtime.split(':')
            dur = data[0][3].split(':')
            dur_hours = int(dur[0]) * 3600
            dur_minutes = int(dur[1]) * 60
            runtime_hours = int(runtime_dur[0]) * 3600
            runtime_minutes = int(runtime_dur[1]) * 60
            total_seconds = runtime_hours + runtime_minutes + int(runtime_dur[2]) + dur_hours + dur_minutes + int(dur[2])
            sec = total_seconds
            hour = sec // 3600
            sec %= 3600
            min = sec // 60
            sec %= 60
            query.exec_(
                f"""UPDATE timeSheet SET end = '{date}', duration = '{"%02d:%02d:%02d" % (hour, min, sec)}' WHERE id = {data[0][0]}"""
            )
