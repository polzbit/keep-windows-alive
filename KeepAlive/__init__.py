from PyQt5.QtWidgets import QApplication
from KeepAlive.windows.MainWindow import MainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from sys import exit as sysExit

def main():
    import sys
    
    def except_hook(cls, exception, traceback):
        print(cls, exception, traceback)
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName(".\\db.sqlite3")
    if not con.open():
        print("Database Error: %s" % con.lastError().databaseText())
        sysExit(0)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow(con)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()