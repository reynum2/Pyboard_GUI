# encoding:utf-8

import os

from PyQt6.QtGui import QFileSystemModel, QAction, QIcon
from PyQt6.QtCore import QDir, QModelIndex, Qt, QFileInfo
from PyQt6.QtWidgets import QTreeView, QMenu, QFileIconProvider

from ui import messages
import src.constant as constant
import src.logger
import src.icons as icons

logger = src.logger.getmylogger(__name__)


class ComputerFileBrowserModel(QFileSystemModel):
    """Used to handle the files and directories on the computer filesystem"""

    def __init__(self, parent: QTreeView) -> None:
        self.parent: QTreeView = parent
        self.current_path = ""
        """The current path where we are"""
        self.allow_erase_file = False
        """Allow the files from the board to erase the one on the computer"""
        super().__init__(self.parent)
        self.setRootPath(QDir.rootPath())
        #self.setRootPath("/home/olivier/Projets")
        self.setFilter(QDir.Filter.NoDot | QDir.Filter.AllDirs | QDir.Filter.AllEntries)
        self.parent.setModel(self)
        self.parent.setColumnWidth(0, 200)
        self.parent.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        #define the treeview as multiline selection with 'ctrl' 
        self.parent.setSelectionMode(self.parent.selectionMode().ExtendedSelection)
        print("QFileSystemModel Icon provider : {}".format(self.iconProvider()))
        self.parent.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setIconProvider(FileIconProvider())
        # Connect the signals
        self.parent.doubleClicked.connect(self.double_click)
        self.parent.customContextMenuRequested.connect(self.right_click_menu)
    
    def right_click_menu(self, position):
        """Triggered when a right click occurred on the computer file browser"""
        indexes: list[QModelIndex] = self.parent.selectedIndexes()
        if len(indexes) == 0:
            logger.debug("No indexes selected")
            return
        if len(indexes) > 0:
            logger.debug("Indexes {}".format(indexes))
        # Create the action menu 
        menu = QMenu()
        copy_act = QAction(icons.get_icon("document-copy"), self.tr("Copy to board"), self)
        # copy_act.setShortcuts(QKeySequence.Open)
        copy_act.setStatusTip(self.tr("Copy an existing file on the board filesystem"))
        copy_act.triggered.connect(lambda: constant.INIT.comm.computer_to_board_copy.emit())
        menu.addAction(copy_act)

        for index in indexes:
            print("dir index :{}".format(dir(index)))
            print("index type :{}".format(self.type(index)))
            # item: str = self.fileName(index)
            print("filename :{}".format(self.fileName(index)))
            print("filepath :{}".format(self.filePath(index)))
        
        menu.exec(self.parent.viewport().mapToGlobal(position))

    def double_click(self, index: QModelIndex):
        """Define the action when a double click is done"""
        self.current_path = self.filePath(index)
        if os.path.isdir(self.current_path):
            if index.data() == "..":
                self.current_path = os.path.dirname(os.path.dirname(self.current_path))
                index = index.parent().parent()
            self.parent.setRootIndex(index)
            constant.INIT.comm.computer_treeview_label.emit(self.current_path)
    
    def write(self, content: bytes, file_name: str) -> str:
        """Create or replace a file on the computer.
        
        The file is created on the current selected path.
        
        Args:
            content (bytes): the content of the file to create
            file_name (str): the name of the file to create

        Return (str):
            A string indicating the copy status

        """
        full_file_name = "{}/{}".format(self.current_path, file_name)
        logger.debug("Full name of file to copy : {}".format(full_file_name))
        # If the file is already present on the computer
        if os.path.isfile(full_file_name) and not self.allow_erase_file:
            btn_clicked = messages.showdialog(
                "The file : {} Already exits \n".format(full_file_name), 
                informative_text="Do you want to replace it ?", 
                icon="Warning", 
                buttons=["Yes", "YesToAll", "No", "Cancel"]
                )
            if btn_clicked == messages.button_type["No"]:
                return "No"
            elif btn_clicked == messages.button_type["YesToAll"]:
                self.allow_erase_file = True
            elif btn_clicked == messages.button_type["Cancel"]:
                return "Cancel"
        # Copy the file on the computer
        return constant.INIT.computer.write(full_file_name, content)

    def get_selected_files(self):
        """List the content of all the items (files and directories) selected
        
        If a directory is selected all subdirectories and files inside will be selected too.

        Return:
            dict{source_path: [file_list]} with the type of the key is also the type of the selected item (file or directory)

        """
        selected_files = {}
        selected_indexes = self.parent.selectedIndexes()
        for selected_index in selected_indexes:
            if not selected_index.isValid() or selected_index.column() != 0:
                continue
            path = self.filePath(selected_index)
            if self.isDir(selected_index):
                selected_files[path] = []
                selected_files.update(constant.INIT.computer.get_files_in_dir(path))
            else:
                selected_files[path] = path
        for source, files in selected_files.items():
            logger.debug("Selected source {}, files : {}".format(source, files))
        return selected_files
    
    def get_selected_size(self):
        """Give the size of the selected items"""
        total_size = 0
        selected_indexes = self.parent.selectedIndexes()
        for selected_index in selected_indexes:
            if not selected_index.isValid() or selected_index.column() != 0:
                continue
            path = self.filePath(selected_index)
            if self.isDir(selected_index):
                total_size += constant.INIT.computer.get_dir_size(path)
            else:
                total_size += constant.INIT.computer.get_file_size(path)
        return total_size
    

class FileIconProvider(QFileIconProvider):
    """To handle the icons of the Treeview"""
    def icon(self, parameter) -> QIcon:
        if parameter.isDir():
            icon = QIcon(icons.get_icon("folder"))
            # This set the icon to show when the treeview branch is open
            icon.addFile("{}/folder-open".format(icons.get_icon_path()), state=QIcon.State.On)
            return icon
        if isinstance(parameter, QFileInfo):
            info = parameter
            if info.suffix() in ["py"]:
                return QIcon(icons.get_icon("python"))
            elif info.suffix() in ["mp4", "avi", "mkv", "mpg", "mpeg", "mov"]:
                return QIcon(icons.get_icon("film"))
            elif info.suffix() in ["sh", "pl"]:
                return QIcon(icons.get_icon("script-text"))
            else:
                return QIcon(icons.get_icon("document-text"))
        return super(FileIconProvider, self).icon(parameter)
