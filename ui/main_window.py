# Form implementation generated from reading ui file 'MainWindows.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(938, 751)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.board_connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.board_connect_button.setObjectName("board_connect_button")
        self.horizontalLayout.addWidget(self.board_connect_button)
        self.list_board_files_button = QtWidgets.QPushButton(self.centralwidget)
        self.list_board_files_button.setObjectName("list_board_files_button")
        self.horizontalLayout.addWidget(self.list_board_files_button)
        self.board_to_computer_button = QtWidgets.QPushButton(self.centralwidget)
        self.board_to_computer_button.setObjectName("board_to_computer_button")
        self.horizontalLayout.addWidget(self.board_to_computer_button)
        self.computer_to_board_button = QtWidgets.QPushButton(self.centralwidget)
        self.computer_to_board_button.setObjectName("computer_to_board_button")
        self.horizontalLayout.addWidget(self.computer_to_board_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.board_browser_label = QtWidgets.QLabel(self.centralwidget)
        self.board_browser_label.setObjectName("board_browser_label")
        self.gridLayout.addWidget(self.board_browser_label, 1, 0, 1, 1)
        self.computer_browser_label = QtWidgets.QLabel(self.centralwidget)
        self.computer_browser_label.setObjectName("computer_browser_label")
        self.gridLayout.addWidget(self.computer_browser_label, 1, 1, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.board_treeView = QtWidgets.QTreeView(self.splitter)
        self.board_treeView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.board_treeView.setObjectName("board_treeView")
        self.computer_treeView = QtWidgets.QTreeView(self.splitter)
        self.computer_treeView.setObjectName("computer_treeView")
        self.console = QtWidgets.QPlainTextEdit(self.splitter_2)
        self.console.setObjectName("console")
        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtGui.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionAvailable = QtGui.QAction(MainWindow)
        self.actionAvailable.setObjectName("actionAvailable")
        self.action_search_board = QtGui.QAction(MainWindow)
        self.action_search_board.setObjectName("action_search_board")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pyboard GUI"))
        self.board_connect_button.setText(_translate("MainWindow", "Connect"))
        self.list_board_files_button.setText(_translate("MainWindow", "list files"))
        self.board_to_computer_button.setToolTip(_translate("MainWindow", "Copy to computer"))
        self.board_to_computer_button.setText(_translate("MainWindow", "→"))
        self.computer_to_board_button.setToolTip(_translate("MainWindow", "copy to board"))
        self.computer_to_board_button.setText(_translate("MainWindow", "←"))
        self.board_browser_label.setText(_translate("MainWindow", "Board file system"))
        self.computer_browser_label.setText(_translate("MainWindow", "Computer file system"))
        self.actionopen.setText(_translate("MainWindow", "Board"))
        self.actionAvailable.setText(_translate("MainWindow", "Available"))
        self.action_search_board.setText(_translate("MainWindow", "Search"))
