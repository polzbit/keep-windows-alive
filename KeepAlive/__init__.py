from PyQt5.QtWidgets import QApplication
from KeepAlive.windows.MainWindow import MainWindow
from KeepAlive.core.db import TimeSheetDb

def main():
    import sys
    db = TimeSheetDb()
    
    def except_hook(cls, exception, traceback):
        print(cls, exception, traceback)
        sys.__excepthook__(cls, exception, traceback)

    # Open the connection

    if not db.isConnectionOpen():
        print("Database Error: %s" % db.lastError().databaseText())
        sys.exit(0)
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow(db)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()