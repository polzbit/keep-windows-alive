from PyQt5.QtWidgets import QApplication
from KeepAlive.windows.MainWindow import MainWindow

def main():
    import sys
    
    def except_hook(cls, exception, traceback):
        print(cls, exception, traceback)
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mw = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()