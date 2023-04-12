# encoding:utf-8

import os

from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction
from PyQt6.QtCore import QModelIndex, Qt, QSortFilterProxyModel
from PyQt6.QtWidgets import QTreeView, QMenu

from ui import messages
import src.constant as constant
import src.logger
import src.icons as icons

logger = src.logger.getmylogger(__name__)

class BoardStandardItem(QStandardItem):
    """Modelize the components of the filesystem like files or directories"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__isdir: bool = False
        """Boolean to define the item as a directory"""
        self.__isfile: bool = False
        """Boolean to define the item as a file"""
        self.__issize: bool = False
        """Boolean to define the item as a file size"""
        self.setEditable(False)
        self.path: str = ""
        """The full (absolute) path of the item"""

    def set_icon(self, icon_name):
        self.setIcon(icons.get_icon(icon_name))

    @property
    def is_dir(self):
        return self.__isdir

    @is_dir.setter
    def is_dir(self, value):
        """Setter for the property is_dir"""
        if value == True:
            self.set_icon("folder")
            self.setIcon(icons.get_icon("folder")) 
        self.__isdir = value

    @property
    def is_file(self):
        return self.__isfile

    @is_file.setter
    def is_file(self, value):
        """Setter for the property is_file"""
        if value == True:
            if self.text().endswith('.py'):
                self.set_icon("python")
            else:
                self.set_icon("script-text")
        self.__isfile = value

    @property
    def is_size(self):
        return self.__issize

    @is_size.setter
    def is_size(self, value):
        """Setter for the property is_size"""
        self.__issize = value


class BoardFileBrowserModel(QStandardItemModel):

    def __init__(self, parent: QTreeView) -> None:
        super().__init__()
        self.file_list = []
        """Contain the list of all files and directories on the filesystem"""
        self._parent: QTreeView = parent
        self.current_directory_parent = None
        """The actual directory while we build the filesystem"""
        self.root_directory = None
        self.current_path = ""
        """The full directory path where the file is when filling the system"""
        self.allow_erase_file = False
        """To inform if we can erase files during a copy without asking each time"""
        self.allow_delete_file = False
        """To inform if we can delete files without asking each time"""
        self.allow_delete_dir = False
        """To inform if we can delete directories without asking each time"""
        super().__init__(0, 2, parent=self._parent)
        #Define the object to sort the directories
        self.proxy_model = SortProxyModel(self)
        self._parent.setModel(self.proxy_model)
        self._parent.setSortingEnabled(True)
        # Connect the double click event signal
        self._parent.doubleClicked.connect(self.double_click)
        # Connect the expand and collapse signals
        self._parent.expanded.connect(self.expand_dir)
        self._parent.collapsed.connect(self.collapse_dir)
        # Set up the right click menu
        self._parent.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._parent.customContextMenuRequested.connect(self.right_click_menu)
        #Define the column names
        self.setHorizontalHeaderLabels(["Name", "Size"])
        #define the treeview as multiline selection with 'ctrl' 
        self._parent.setSelectionMode(self._parent.selectionMode().ExtendedSelection)
        #define the width of the column "Name"
        self._parent.setColumnWidth(0, 200)

    def expand_dir(self, index: QModelIndex) -> None:
        """action to do when a directory is expanded, here change the directory icon"""
        initial_index = self.proxy_model.mapToSource(index)
        item:BoardStandardItem = self.itemFromIndex(initial_index)
        item.set_icon("folder-open")
    
    def collapse_dir(self, index: QModelIndex) -> None:
        """action to do when a directory is collapsed, here change the directory icon"""
        initial_index = self.proxy_model.mapToSource(index)
        item:BoardStandardItem = self.itemFromIndex(initial_index)
        item.set_icon("folder")

    def right_click_menu(self, position):
        """Open the menu available with mouse right clic"""
        #Get the items selected
        indexes: list[QModelIndex] = self._parent.selectedIndexes()
        if len(indexes) == 0:
            return
        else:
            print("indexes : {}".format(indexes))
        for index in indexes:
            print("index :{}".format(index))
            print("index column :{}".format(index.column()))
            print("index data :{}".format(index.data()))
            print("index isvalid :{}".format(index.isValid()))
            if index.column == 1:
                continue
        menu = QMenu(self._parent)
        # Copy action
        copy_icon = icons.get_icon("document-copy")
        copy_act = QAction(copy_icon, self.tr("Copy to computer"), self)
        # copy_act.setShortcuts(QKeySequence.Open)
        copy_act.setStatusTip(self.tr("Copy an existing file on the computer filesystem"))
        copy_act.triggered.connect(lambda: constant.INIT.comm.board_to_computer_copy.emit())
        menu.addAction(copy_act)
        # Delete action
        delete_act = QAction(icons.get_icon("bin-metal"), self.tr("Delete"), self)
        delete_act.triggered.connect(self.delete)
        menu.addAction(delete_act)
        
        menu.exec(self._parent.viewport().mapToGlobal(position))
    
    def delete(self, _) -> str:
        """Delete the file(s) and the directory(ies) selected"""
        selected_items = self.get_selected_items()
        for item in selected_items:
            if not isinstance(item, BoardStandardItem):
                continue
            # Delete a directory
            if item.is_dir:
                dir_to_delete = item.path
                if not self.allow_delete_dir:
                    btn_clicked = messages.showdialog(
                        "Do you want to delete the directory and everything inside \"{}\"".format(dir_to_delete), 
                        informative_text="This cannot be undone", 
                        icon="Warning", 
                        buttons=["Yes", "YesToAll", "No", "Cancel"]
                    )
                    if btn_clicked == messages.button_type["No"]:
                        continue
                    elif btn_clicked == messages.button_type["YesToAll"]:
                        self.allow_delete_dir = True
                    elif btn_clicked == messages.button_type["Cancel"]:
                        return "Cancel"
                constant.INIT.board.delete_dir(dir_to_delete)
            # Delete a file
            if item.is_file:
                file_to_delete = os.path.join(item.path, item.text())
                if not self.allow_delete_file:
                    btn_clicked = messages.showdialog(
                        "Do you want to delete the file \"{}\"".format(file_to_delete), 
                        informative_text="This cannot be undone", 
                        icon="Warning", 
                        buttons=["Yes", "YesToAll", "No", "Cancel"]
                    )
                    if btn_clicked == messages.button_type["No"]:
                        continue
                    elif btn_clicked == messages.button_type["YesToAll"]:
                        self.allow_delete_file = True
                    elif btn_clicked == messages.button_type["Cancel"]:
                        return "Cancel"
                constant.INIT.board.delete_file(file_to_delete)
        self.allow_delete_file = False
        self.allow_delete_dir = False
        self.refresh()

    def get_dir_content(self, directory):
        """Return all the content of the given directory
        
        Args:
            directory (str): the path of the directory to get

        Return:
            (list(tuple)) all the content of the directory 
            The form of the tuple is (full_name, type, inode, size)
            - type is 0x4000 for directories and 0x8000 for regular files
            The list is flatten (the tree structure is removed)
        
        """
        dir_content = constant.INIT.board.list_files(directory)
        flat_dir_content = []
        def flat_file_list(file_list):
            """Used to have a 1D list with elements inside, instead of a nD list"""
            for n, file_ in enumerate(file_list):
                if len(file_) == 0:
                    continue
                if file_[1] == 0x8000:
                    flat_dir_content.append(file_)
                elif file_[1] == 0x4000:
                    flat_dir_content.append(file_)
                    try:
                        flat_file_list(file_list[n+1])
                    except:
                        return
        flat_file_list(dir_content)
        return flat_dir_content
    
    def get_selected_files(self) -> list:
        """Return all the files and directories selected"""
        selected_items = self.get_selected_items()
        output_list = []
        for item in selected_items:
            if not isinstance(item, BoardStandardItem):
                continue
            if item.is_dir:
                output_list.append(constant.INIT.board.file_info(item.path))
                output_list.append(constant.INIT.board.list_files(directory=item.path))
            if item.is_file:
                output_list.append(constant.INIT.board.file_info("{}/{}".format(item.path,item.text())))
        return output_list

    def get_selected_items(self) -> list[BoardStandardItem]:
        """Returns the items selected by the user"""
        selected_items = []
        selected_indexes = self._parent.selectionModel().selectedIndexes()
        for selected_index in selected_indexes:
            if not selected_index.isValid():
                continue
            selected_index = self.proxy_model.mapToSource(selected_index)
            selected_items.append(self.itemFromIndex(selected_index))
        return selected_items

    def refresh(self):
        """Clear the board treeview and recreate again (do a refresh)"""
        # self.clear()
        self.fill_data()

    def double_click(self, index: QModelIndex):
        """Define the action when a double click is done"""
        initial_index = self.proxy_model.mapToSource(index)
        item:BoardStandardItem = self.itemFromIndex(initial_index)
        if item is not None and item.is_dir:
            if item.text() == "..":
                index = index.parent().parent()
            self._parent.setRootIndex(index)
            # Get the new root path item
            new_index = self.proxy_model.mapToSource(index)
            new_item:BoardStandardItem = self.itemFromIndex(new_index)
            if new_item is not None:
                # Emit the signal to print the current path in the label
                constant.INIT.comm.board_treeview_label.emit(new_item.path)
                self.current_path = new_item.path
            else:
                constant.INIT.comm.board_treeview_label.emit("/")
                self.current_path = "/"
        if item is not None and not item.is_dir:
            logger.debug("Full path of the double clicked file : {}".format(item.path))

    def create_file_structure(self, file_list):
        """Will create the tree structure in accordance with the files and directories on the board"""
        if self.current_directory_parent is None:
            self.current_directory_parent = self.root_directory = self.invisibleRootItem()
            self.current_path = "/"
        logger.debug("File list for creating the structure: {}".format(file_list))
        for n, file_ in enumerate(file_list):
            # If the directory is empty
            if len(file_) <= 1 :
                logger.debug("Empty directory")
                continue
            if file_[1] == 0x4000:
                logger.debug("Directory : {}".format(file_))
                # Because the file name is absolute by default
                simple_file_name = os.path.basename(file_[0])
                two_dots = BoardStandardItem("..")
                two_dots.is_dir = True
                new_parent = BoardStandardItem(simple_file_name)
                new_parent.is_dir = True

                self.current_directory_parent.appendRow(new_parent)
                self.current_directory_parent = new_parent
                self.current_directory_parent.appendRow(two_dots)
                self.current_path = os.path.join(self.current_path, simple_file_name)
                # Define the path of the actual directory
                new_parent.path = self.current_path
                # Recursive call
                self.create_file_structure(file_list[n+1])
            elif file_[1] == 0x8000:
                logger.debug("File : {}".format(file_))
                file_name = BoardStandardItem(os.path.basename(file_[0]))
                file_name.path = self.current_path
                file_name.is_file = True
                file_size = BoardStandardItem(str(file_[3]))
                file_size.is_size = True
                self.current_directory_parent.appendRow([file_name, file_size ])
        if self.current_directory_parent is not None:
            # Because the root directory is none when called by parent() so we need to set manually
            if self.current_directory_parent.parent():
                self.current_directory_parent = self.current_directory_parent.parent()
            else:
                self.current_directory_parent = self.root_directory
            self.current_path = os.path.dirname(self.current_path)

    def mkdir(self, path):
        """Create a directory on the board, where we are"""
        constant.INIT.board.mkdir(os.path.join(self.current_path, path))
    
    def write(self, content: str, file_name: str) -> str:
        """Create or replace a file on the board.
        
        The file is created on the current selected path.
        
        Args:
            content (str): the content of the file to create (need to be in format 2 hex per bytes)
            file_name (str): the full name of the file to create

        Return (str):
            A string indicating the copy status

        """
        full_file_name = "{}/{}".format(self.current_path, file_name)
        logger.debug("Full name of file to copy : {} to the board".format(full_file_name))
        # If the file is already present on the computer
        if constant.INIT.board.is_file(full_file_name) and not self.allow_erase_file:
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
        # Copy the file on the board
        return constant.INIT.board.write(full_file_name, content)

    def fill_data(self):
        """Print the files present in the board"""
        self.setRowCount(0)
        self.current_directory_parent = None
        self.create_file_structure(constant.INIT.board.list_files())

    def isDir(self, index: QModelIndex) -> bool:
        item:BoardStandardItem = self.itemFromIndex(index)
        return item.is_dir


class SortProxyModel(QSortFilterProxyModel):
    """Sorting proxy model that always places folders on top."""
    def __init__(self, model:BoardFileBrowserModel):
        super().__init__()
        self.source_model = model
        self.setSourceModel(model)

    def lessThan(self, left: QModelIndex, right: QModelIndex):
        """Perform sorting comparison ( is equivalent to < ).

        Since we know the sort order, we can ensure that folders always come first.

        Returns:
            True if left < right.
            Else False
        """
        item_left:BoardStandardItem = self.source_model.itemFromIndex(left)
        item_right:BoardStandardItem = self.source_model.itemFromIndex(right)
        if not isinstance(item_left, BoardStandardItem):
            return False
        if not isinstance(item_right, BoardStandardItem):
            return True
        left_data = item_left.text()
        right_data = item_right.text()
        left_is_folder = item_left.is_dir
        right_is_folder = item_right.is_dir
        sort_order = self.sortOrder()

        if left_data == "..":
            return False
        if right_data == "..":
            return True

        if left_is_folder and not right_is_folder:
            result = sort_order == Qt.SortOrder.AscendingOrder
        elif not left_is_folder and right_is_folder:
            result = sort_order != Qt.SortOrder.AscendingOrder
        else:
            result = left_data < right_data
        return result