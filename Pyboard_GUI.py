#! /usr/bin/env python3
# encoding:utf-8

import sys

from PyQt6 import QtWidgets

import src.constant as constant
from src.init import Init

from ui.main_window import Ui_MainWindow

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # Initialize the main window 
    constant.INIT = Init(ui)
    app.aboutToQuit.connect(constant.INIT.close_window)
    # Load the behaviour of the widgets
    MainWindow.show()
    # Start the app
    out = app.exec()
    sys.exit(out)