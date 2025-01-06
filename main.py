import sys
from app.controller import MainWindowController
from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindowController(app)
    main_window.showFullScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
