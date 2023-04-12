"""This file the logging handler"""
# encoding:utf-8

import logging
import os

CONS_LOG_LEVEL: str = "DEBUG"
"""Define the logging level for the console, values can be : CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET"""

FILE_LOG_LEVEL: str = "INFO"
"""Define the logging level for the log file, values can be : CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET"""

MAIN_PATH: str = os.path.dirname(os.path.abspath(__file__))
"""The main path of the application"""

def getmylogger(name):
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - Module:%(module)s - Function:%(funcName)s : %(message)s')
    console_formatter = logging.Formatter('%(levelname)s -- %(message)s')
    
    file_handler = logging.FileHandler("{}/../{}".format(MAIN_PATH, "logfile.log"))
    file_handler.setLevel(FILE_LOG_LEVEL)
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONS_LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
    return logger