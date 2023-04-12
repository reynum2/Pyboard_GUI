# encoding:utf-8

from ast import literal_eval
from serial.tools import list_ports

import src.constant as constant
import src.pyboard as pyboard
import src.logger

logger = src.logger.getmylogger(__name__)

class Board():

    def __init__(self) -> None:
        self.connected_board = None
        self.board_lst = []
        self.file_list = []

    def detect_board(self) -> None:
        """"Check if a compatible board is present.
        
        The boards connected to the computer will be register in self.board_lst.

        """
        self.board_lst = []
        for port in list_ports.comports():
            if "USB" in port.hwid:
                self.board_lst.append(port)
        if not self.board_lst:
            self.connected_board = None

    def connect(self, board_num, baud_rate=115200) -> None:
        """Connect to the board 
        
        Args:
            board_num (int): The index in the board list

        """
        try:
            self.connected_board = pyboard.Pyboard(self.board_lst[board_num].device, baud_rate)
        except Exception as exc:
            print(exc)

    def disconnect(self) -> None: 
        """Correctly close the connection"""
        if not self.connected_board:
            logger.info("Cannot disconnect an unconnected board")
            return
        try:
            #In case of the board is still in raw repl mode
            self.connected_board.exit_raw_repl()
            #Close the connection
            self.connected_board.close()
            logger.info("close the connection")
        except Exception as exc:
            logger.error(exc)
    
    def send_command(self, command) -> str:
        """Entre in Raw repl mode send the command and exit raw repl
        
        Args:
            command (str): python script to execute on the board

        Return:
            the strings print by the python script executed on the board

        """
        logger.debug("Send to the board the command : {}".format(command))
        self.connected_board.enter_raw_repl()
        ret = self.connected_board.exec(command)
        self.connected_board.exit_raw_repl()
        return ret
    
    def delete_file(self, file):
        """Delete the given file from the board filesystem
        
        Args:   
            file (str): Full path to the file to delete

        """
        # Because on windows they are using backslash instead on standard slash
        file = file.replace("\\", "/")
        logger.debug("Delete directory : {}".format(file))
        try:
            ret = self.send_command(constant.DELETE.replace("FILENAME", file)).decode()
        except Exception as ex:
            logger.error("Cannot delete directory : {}, {}".format(ret, ex))
        return ret
    
    def delete_dir(self, dir):
        """Delete recursively the given directory from the board filesystem
        
        Args:   
            dir (str): Full path to the directory to delete

        """
        # Because on windows they are using backslash instead on standard slash
        dir = dir.replace("\\", "/")
        logger.debug("Delete directory : {}".format(dir))
        try:
            ret = self.send_command(constant.DELETEDIR.replace("FILENAME", dir)).decode()
        except Exception as ex:
            logger.error("Cannot delete directory : {}, {}".format(ret, ex))
        return ret
    
    def list_files(self, directory="/") -> list:
        """List the files present in the board
        
        Return:
            A list of tuple of the files in the board
            The tuple structure is ('file_name', type, inode, size) 
            - type is 0x4000 for directories and 0x8000 for regular files

        """
        if not self.connected_board:
            return None
        # Because on windows they are using backslash instead on standard slash
        directory = directory.replace("\\", "/")
        ret_str = self.send_command(constant.ILISTDIR.replace("PATH", directory)).decode()
        ret_lst = self.file_list = literal_eval(ret_str)
        return ret_lst

    def is_file(self, file_name) -> bool:
        """Test if the file is regular and is present on the board filesystem"""
        # Because on windows they are using backslash instead on standard slash
        file_name = file_name.replace("\\", "/")
        ret = self.file_info(file_name)
        if ret is None:
            return False
        elif ret[1] == 0x8000:
            return True
        else:
            return False
        
    def is_dir(self, file_name) -> bool:
        """Test if the file is a directory and is present on the board filesystem"""
        # Because on windows they are using backslash instead on standard slash
        file_name = file_name.replace("\\", "/")
        ret = self.file_info(file_name)
        if ret is None:
            return False
        elif ret[1] == 0x4000:
            return True
        else:
            return False

    def file_info(self, file_name: str) -> list:
        """Get the information of a file or directory in the same format as list_files does
        
        Args:
            file_name (str): the full path of the file

        Return:
            (list) : The informations of the file or directory
            None if it does not exists

        """
        # Because on windows they are using backslash instead on standard slash
        file_name = file_name.replace("\\", "/")
        ret:str = self.send_command(constant.FILEINFOS.replace("FILENAME", file_name)).decode()
        logger.debug("Info of the file {} are : {}".format(file_name, ret))
        if ret.find("Errno") == 1:
            print("File not found on the board : {}".format(ret))
            return None
        return literal_eval(ret)
    
    def send_file(self, file_name: str) -> str:
        """Ask the board to send the content of a file.
        
        Args:
            file_name (str): the full path name of the file on the board
        
        Return:
            (str) the content of the file in format 2 hexadecimal digits per byte

        """
        # Because on windows they are using backslash instead on standard slash
        file_name = file_name.replace("\\", "/")
        logger.info("Ask board to send the content of the file {}".format(file_name))
        command = constant.SENDFILE.replace("FILENAME", file_name)
        # get the file value as string
        file_content = self.send_command(command).decode("utf-8")
        logger.debug("file content in hexlify format = {}".format(file_content))
        return file_content

    def mkdir(self, dir_name: str) -> bool:
        """Create a directory on the board

        Args:
            dir_name (str): the absolute path of the directory to create
        
        Return:
            False (bool) if something went wrong else True

        """
        # Because on windows they are using backslash instead on standard slash
        dir_name = dir_name.replace("\\", "/")
        ret:str = self.send_command(constant.MKDIR.replace("DIRNAME", dir_name)).decode()
        if ret.find("Errno 17") == 1:
            logger.error("The directory {} already exists on the board : {}".format(dir_name, ret))
            return False
        if ret.find("Errno 2") == 1:
            logger.error("The directory path contain a wrong name : {}".format(dir_name))
            return False
        return True
    
    def flash_free_size(self) -> int:
        """Give the free space of the flash memory
        
        Return:
            (int) the free space of the flash

        """
        ret:str = self.send_command(constant.FLASHFREESIZE).decode()
        return int(ret)
    
    def write(self, file_name: str, content: str):
        """Write a file on the board
        
        Args:
            file_name (str): the full name of the file to create
            content (bytes): The content in format 2 hexadecimal digits per byte

        """
        # Because on windows they are using backslash instead on standard slash
        file_name = file_name.replace("\\", "/")
        command_to_send = constant.WRITE.replace("FILENAME", file_name)
        command_to_send = command_to_send.replace("CONTENT", content)
        return self.send_command(command_to_send).decode()
