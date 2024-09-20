from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pandas as pd
from datetime import datetime
from sys import exit as sysExit
from .calendar import get_runtime_time
class TimeSheetDb:
    def __init__(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        if not self.con.open():
            print("Database Error: %s" % self.con.lastError().databaseText())
            sysExit(0)
        self.con.setDatabaseName(".\\AppDb")
    
    def lastError(self):
        return self.con.lastError()
    
    def isConnectionOpen(self):
        return self.con and self.con.open()
    
    def closeConnection(self):
        self.con.close()
        del self.con
        self.con = None
        QSqlDatabase.removeDatabase("QSQLITE")
        sysExit(0)
    
    def clearTimeSheetTable(self):
        query = QSqlQuery()
        query.exec('delete from timeSheet')
        query.finish()
    
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
        query = QSqlQuery()
        query.exec(
            """
            CREATE TABLE timeSheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                start TIMESTAMP NOT NULL,
                end TIMESTAMP,
                duration VARCHAR(40)
            )
            """
        )
        query.finish()
    
    def createTimestamp(self, runtime, end):
        date = pd.to_datetime(datetime.now())
        query = QSqlQuery()
        data = self.getTimeSheet(date, True)
        if(not end and not len(data)):
            query.exec(
                f"""INSERT INTO timeSheet (start)
                VALUES ('{date}')"""
            )
            query.finish()
        elif end and len(data):
            total_seconds = get_runtime_time(runtime)
            sec = total_seconds
            hour = sec // 3600
            sec %= 3600
            min = sec // 60
            sec %= 60
            query.exec_(
                f"""UPDATE timeSheet SET end = '{date}', duration = '{"%02d:%02d:%02d" % (hour, min, sec)}' WHERE id = {data[0][0]}"""
            )
            query.finish()
