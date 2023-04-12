# encoding:utf-8

import os
import binascii

from ui import messages

import src.constant as constant
import src.logger

logger = src.logger.getmylogger(__name__)

class Computer():
    """Handle operation on the computer filesystem"""

    def __init__(self) -> None:
        self.connected_board = None
        self.board_lst = []
        self.file_list = []

    def write(self, path, content):
        """Write a file on the computer filesystem
        
        Args:
            path (str): the full file name to write
            content (byte): the data of the file in hexlify format

        Return:
            (str): Ok or Impossible
        
        """
        try:
            content_to_write = bytes.fromhex(content)
            logger.debug("Content of file {} to write on the board : {}".format(path, content_to_write))
            with open(path, "wb") as file_on_computer:
                file_on_computer.write(content_to_write)
            
        except Exception as ex:
            messages.showdialog(
                "Error cannot write the file : \n{}".format(ex), 
                informative_text="Try another directory", 
                icon="Warning", 
                buttons=["Ok"]
                )
            print("Error cannot write the file : {}".format(ex))
            return "Impossible"
        return "Ok"


    def mkdir(self, dir_to_create: str, path_where_to_create: str) -> bool:
        """Create a directory in the current path of the treeview
        
        Open a message box if the creation fail

        Args:
            dir_to_create (str): The path to create inside the current path
            path_where_to_create (str): the path on the computer where the directory will be created
        
        Return:
            (bool) : True if the directory has been created else False
        """
        try:
            logger.debug("Create the directory \"{}\" on the computer at the place \"{}\"".format(dir_to_create, path_where_to_create))
            os.mkdir(os.path.join(path_where_to_create,dir_to_create))
            return True
        except Exception as ex:
            logger.error("cannot create the directory {}, Reason : {}".format(dir_to_create, ex))
            messages.showdialog(
                "Error cannot create the directory \"{}\" in this path \n Error : {}".format(dir_to_create, ex),
                informative_text="Try another directory",
                icon="Warning",
                buttons=["Ok"]
            )
            return False
    
    def get_files_in_dir(self, path):
        """Get all files and directories recursively inside the given path
        
        Args:
            path (str) : The source path for the recursive walk

        Return:
            dict{dir_path: [file_list]} : A list containing all the child files of the path

        """
        file_list = {}
        for root, subdirs, files in os.walk(path):
            if subdirs:
                for sd in subdirs:
                    file_list[os.path.join(root, sd)] = []
                    self.get_files_in_dir(os.path.join(root, sd))
            if files:
                file_list[root] = files
        return file_list

    def get_dir_size(self, path):
        """Return the full size of the given path"""
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += entry.stat().st_size
                    total += self.get_dir_size(entry.path)
        return total
    
    def get_file_size(self, path) -> int:
        """Give the size of a single file
        
        Args:
            path (str): the full path to the file

        Return:
            (int) the size of the file

        """
        try:
            size = os.path.getsize(path)
        except Exception as ex:
            logger.error("Cannot get the size of file : {}".format(path))
        return size
    
    def send_file(self, path: str) -> str:
        """Convert the given file into a format nice to be transfered"""
        content = None
        try:
            with open(path, 'rb') as f:
                f_content = f.read()
                content = binascii.hexlify(f_content)
        except Exception as ex:
            logger.error("Cannot send the file {}\nerror : {}".format(path, ex))
            return
        return content.decode()