"""This file contain the action called when clicking on the GUI"""
# encoding:utf-8

import os

from ui.main_window import Ui_MainWindow
from ui import messages
from src.board_file_browser_model import BoardStandardItem

import src.constant as constant
import src.logger

logger = src.logger.getmylogger(__name__)


class Behaviour():

    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.ui.board_connect_button.clicked.connect(self.connect_button_clicked)
        self.ui.list_board_files_button.clicked.connect(self.list_board_files_button_clicked)
        self.ui.board_to_computer_button.clicked.connect(self.board_to_computer_copy)

    def connect_button_clicked(self, event):
        """Define the action when the connect button is clicked
        """
        if len(constant.INIT.board.board_lst) == 0 and not constant.INIT.board.connected_board:
            constant.INIT.board.detect_board()
        elif len(constant.INIT.board.board_lst) != 0 and not constant.INIT.board.connected_board:
            logger.debug("Board list : {}".format(type(constant.INIT.board.board_lst[0])))
            constant.INIT.board.connect(0)
            if constant.INIT.board.connected_board:
                self.ui.statusbar.showMessage("Board Connected on {}".format(constant.INIT.board.connected_board.serial.port), 5000)
        elif len(constant.INIT.board.board_lst) == 0:
            self.ui.statusbar.showMessage("No board found", 5000)
        elif constant.INIT.board.connected_board:
            self.ui.statusbar.showMessage("One board is already connected on {}".format(constant.INIT.board.connected_board.serial.port), 5000)
    
    def update_computer_label(self, path: str):
        """Print the current path in the label on top of the Computer treeview"""
        self.ui.computer_browser_label.setText("Computer file system : {}".format(path))

    def update_board_label(self, path: str):
        """Print the current path in the label on top of the Board treeview"""
        self.ui.board_browser_label.setText("Board file system : {}".format(path))

    def list_board_files_button_clicked(self):
        """List the files present in the board"""
        if not constant.INIT.board.connected_board:
            self.ui.statusbar.showMessage("No board connected", 5000)
            return
        try:
            logger.debug("Try to connect to the board")
            constant.INIT.board_browser_model.refresh()
        except Exception as ex:
            logger.warn("Cannot list the files : {}".format(ex))
            messages.showdialog(
                "Cannot list the files : {}".format(ex), 
                icon="Critical", 
                buttons=["Close"]
            )
            return            

    def board_to_computer_copy(self):
        """Copy the selected files and directories from the board to the computer filesystem"""
        if not constant.INIT.board.connected_board:
            self.ui.statusbar.showMessage("No board connected", 5000)
            return
        selected_items = constant.INIT.board_browser_model.get_selected_items()
        for item in selected_items:
            if not isinstance(item, BoardStandardItem):
                continue
            if item.is_dir:
                path_prefix, dir_to_create = os.path.split(item.path)
                # get the whole content of the current directory
                dir_content = constant.INIT.board_browser_model.get_dir_content(item.path)
                if not os.path.isdir(os.path.join(constant.INIT.computer_browser_model.current_path, dir_to_create)):
                    # create the top directory on the computer
                    constant.INIT.computer.mkdir(dir_to_create, constant.INIT.computer_browser_model.current_path)
                for content in dir_content:
                    # if the content is a file
                    if content[1] == 0x8000:
                        self.board_to_computer_copy_file(content[0], from_dir=True)
                    # If the content is a directory
                    if content[1] == 0x4000:
                        # create the subdirectories
                        sub_dir_to_create = os.path.relpath(content[0], start=path_prefix)
                        if not os.path.isdir(os.path.join(constant.INIT.computer_browser_model.current_path, sub_dir_to_create)):
                            # create the top directory on the computer
                            constant.INIT.computer.mkdir(sub_dir_to_create, constant.INIT.computer_browser_model.current_path)
            elif item.is_file:
                full_file_name = os.path.join(item.path, item.text())
                self.board_to_computer_copy_file(full_file_name)
        # Reset the boolean 
        constant.INIT.computer_browser_model.allow_erase_file = False

    def board_to_computer_copy_file(self, file_name: str, from_dir: bool=False):
        """Ask the board to send the content of a file, and ask the computer to write this content in a file
        
        Args:   
            file_name (str): The full path of the file on the board
            from_dir (bool): if the file come from a copy of a directory we must keep his full path

        """
        #Ask the board to send the content of the file
        file_content = constant.INIT.board.send_file(file_name)
        if not from_dir:
            # Keep only the name of the file
            _, file_name = os.path.split(file_name)
        #Copy the content to the computer
        return constant.INIT.computer_browser_model.write(file_content, file_name)

    def computer_to_board_copy(self):
        """Copy the selected files and directories from computer to the board"""
        if not constant.INIT.board.connected_board:
            self.ui.statusbar.showMessage("No board connected", 5000)
            return
        # Test if there is enough free space on the board
        board_free_space = constant.INIT.board.flash_free_size()
        selected_files_size = constant.INIT.computer_browser_model.get_selected_size()
        if selected_files_size > board_free_space:
            logger.warn("Not enough free space on the board")
            messages.showdialog(
                "Not enough free space on the board", 
                icon="Warning", 
                buttons=["Close"]
            )
            return
        # Get the file(s) and directory(ies) to copy
        selected_computer_files = constant.INIT.computer_browser_model.get_selected_files()
        path_prefix = constant.INIT.computer_browser_model.current_path
        for origin, files in selected_computer_files.items():
            logger.debug("Copy to board origin : {}, file : {}".format(origin, files))
            if os.path.isdir(origin):
                dir_selected = os.path.relpath(origin, start=path_prefix)
                logger.debug("Write to board directory : {}".format(dir_selected))
                constant.INIT.board_browser_model.mkdir(dir_selected)
            # In the case files are in a list (and so inside a directory)
            if isinstance(files, list):
                for file in files:
                    if os.path.isfile(os.path.join(origin, file)):
                        dir_selected = os.path.relpath(origin, start=path_prefix)
                        file_selected = os.path.basename(file)
                        self.computer_to_board_copy_file(os.path.join(origin, file), os.path.join(dir_selected, file_selected))
            # In the case files is a path (and is a single file)
            elif os.path.isfile(files):
                _, file_selected = os.path.split(files)
                logger.debug("File selected {}".format(file_selected))
                self.computer_to_board_copy_file(files, file_selected)

    def computer_to_board_copy_file(self, file_on_computer, file_on_board):
        """Copy the file from the computer on the board"""
        if not os.path.isfile(file_on_computer):
            logger.error("the file \"{}\" does not exists on the computer")
            return
        #Ask the computer to send the content of the file
        logger.debug("Read the content of the file {}".format(file_on_computer))
        file_content = constant.INIT.computer.send_file(file_on_computer)
        #Copy the content to the board
        logger.debug("Create or replace the file {} on the board".format(file_on_board))
        return constant.INIT.board_browser_model.write(file_content, file_on_board)