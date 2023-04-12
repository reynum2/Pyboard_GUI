# encoding:utf-8

import os

from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from ui.main_window import Ui_MainWindow

from src.computer_file_browser_model import ComputerFileBrowserModel
from src.board_file_browser_model import BoardFileBrowserModel
from src.board import Board
from src.computer import Computer
from src.behaviour import Behaviour
import src.logger

logger = src.logger.getmylogger(__name__)

class Init():
    """Initialize all the components of the software and keep references on them
    """

    def __init__(self, ui: Ui_MainWindow) -> None:
        self.ui = ui
        """This object represents all the gui widgets"""
        self.behaviour = Behaviour(self.ui)
        """The object containing the behaviour when interacting with the ui"""
        self.board = Board()
        """This object aim to control the actions on the connected ESP32 board"""
        self.computer = Computer()
        """Object to make operations on the computer filesystem"""
        self.check_boards()
        # The check board is call every 2 seconds to check deconnection or new connection
        self.check_boards_timer = QTimer()
        self.check_boards_timer.timeout.connect(self.check_boards)
        self.check_boards_timer.start(2000)
        # Create the custom treeviews
        self.computer_browser_model: ComputerFileBrowserModel = ComputerFileBrowserModel(self.ui.computer_treeView)
        # self.init_computer_browser()
        self.board_browser_model: BoardFileBrowserModel = BoardFileBrowserModel(self.ui.board_treeView)
        self.comm = Communicate()
        """The communication object where the signals are define"""
        self.comm.board_to_computer_copy.connect(self.behaviour.board_to_computer_copy)
        self.comm.computer_to_board_copy.connect(self.behaviour.computer_to_board_copy)
        self.comm.computer_treeview_label.connect(self.behaviour.update_computer_label)
        self.comm.board_treeview_label.connect(self.behaviour.update_board_label)

    def check_boards(self):
        """Check if a board is connected"""
        self.board.detect_board()
        if not self.board.board_lst:
            self.ui.statusbar.showMessage("No board found", 3000)

    def close_window(self):
        """For the board connection to be correctly closed when the window close."""
        self.board.disconnect()




class Communicate(QObject):
    """Class to define the signals to communicate inside the software"""

    board_to_computer_copy = pyqtSignal()
    """the signal to copy files and folders from board to the computer filesystem """
    computer_to_board_copy = pyqtSignal()
    """the signal to copy files and folders from computer to the board filesystem """
    board_treeview_label = pyqtSignal(str)
    """the signal to print the actual path of the board filesystem in the label on top of the treeview"""
    computer_treeview_label = pyqtSignal(str)
    """the signal to print the actual path of the computer filesystem in the label on top of the treeview"""

    def __init__(self) -> None:
        super().__init__()

        