from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pandas as pd
from datetime import datetime
from sys import exit as sysExit
from os import path 

class TimeSheetDb:
    def __init__(self):
        self.projectId = None
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        if not path.isfile(".\\db.sqlite3"):
            self.openConnection()
            self.createTables()
        else:
            self.openConnection()
    
    def openConnection(self):
        self.con.setDatabaseName(".\\db.sqlite3")
        if not self.con.open():
            print("Database Error: %s" % self.con.lastError().databaseText())
            sysExit(0)
    
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
    
    def getTimeSheet(self, date: pd.Timestamp = pd.to_datetime(datetime.now()), byDay = False):
        query = QSqlQuery()
        monthText = f'0{date.month}'
        dayText = f'0{date.day}'
        if(date.month > 9):
            monthText = f'{date.month}'
        if(date.day > 9):
            dayText = f'{date.day}'
        if(byDay):
            query.exec(f"SELECT id, start, end, duration FROM timeSheet WHERE project_id = {self.projectId} AND strftime('%m', start) = '{monthText}' AND strftime('%Y', start) = '{date.year}' AND strftime('%d', start) = '{dayText}'") 
        else:
            query.exec(f"SELECT id, start, end, duration FROM timeSheet WHERE project_id = {self.projectId} AND strftime('%m', start) = '{monthText}' AND strftime('%Y', start) = '{date.year}'")
        id, start, end, duration = range(4)
        data = []
        while query.next():
            data.append((query.value(id), query.value(start), query.value(end), query.value(duration)))
        query.finish()
        return data
    
    def createTables(self):
        query = QSqlQuery()
        query.exec(
            """
            CREATE TABLE timeSheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                start TIMESTAMP NOT NULL,
                end TIMESTAMP,
                duration VARCHAR(40),
                project_id INTEGER
            )
            """
        )
        query.exec(
            """
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(140)
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
                f"""INSERT INTO timeSheet (start, project_id)
                VALUES ('{date}', {self.projectId})"""
            )
            query.finish()
        elif end and len(data):
            query.exec_(
                f"""UPDATE timeSheet SET end = '{date}', duration = '{runtime}' WHERE id = {data[0][0]}"""
            )
            query.finish()


    def updateTimestamp(self, date, start, end, duration):
        currentDate = pd.to_datetime(date, dayfirst=True)
        startDate = pd.to_datetime(f"{currentDate.year}/{currentDate.month}/{currentDate.day} {start}")
        endDate = pd.to_datetime(f"{currentDate.year}/{currentDate.month}/{currentDate.day} {end}")
        query = QSqlQuery()
        data = self.getTimeSheet(startDate, True)
        if(not len(data)):
            query.exec(
                f"""INSERT INTO timeSheet (start, end, duration, project_id)
                VALUES ('{startDate}','{endDate}', '{duration}', {self.projectId})"""
            )
            query.finish()
        else:
            query.exec_(
                f"""UPDATE timeSheet SET start = '{startDate}', end = '{endDate}', duration = '{duration}' WHERE id = {data[0][0]}"""
            )
            query.finish()
    
    def getProjects(self):
        query = QSqlQuery()
        query.exec(f"SELECT id, name FROM projects")
        id, name = range(2)
        data = []
        while query.next():
            data.append((query.value(id), query.value(name)))
        query.finish()
        self.projectId = data[0][0]
        return data

    def setProjectIdByName(self, name:str):
        query = QSqlQuery()
        query.exec(f"SELECT id FROM projects WHERE name = '{name}'")
        query.next()
        self.projectId = query.value(0)
        query.finish()
    
    def createProject(self, name:str):
        query = QSqlQuery()
        query.exec(
                f"""INSERT INTO projects (name)
                VALUES ('{name}')"""
            )
        query.finish()
        
            
