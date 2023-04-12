"""This file must contain all the constants and also the object shared in many places in the software"""
# encoding:utf-8

import os

from src.init import Init

# A Reference on the init object
INIT: Init = None
"""This object contains the objects created during the launch of the software"""

MAIN_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LISTDIR: str = """
import os
try:
    print(os.listdir(PATH))
except Exception as ex:
    print(Errno: {}".format(ex))
"""
"""List the content of a directory"""

ILISTDIR: str = """
import os
def ilist_dir(path):
    ret = []
    if not path.endswith("/"):
        path += "/"
    for file_ in os.ilistdir(path):
        file_ = list(file_)
        file_[0] = path + file_[0]
        if file_[1] == 0x4000:
            ret.append(file_)
            ret.append(ilist_dir(file_[0]))
        else:
            ret.append(file_)
    return ret
print(ilist_dir('PATH'))
"""
"""List recursively the content of a directory"""

SENDFILE: str = """
import ubinascii
import sys
content = ""
with open("FILENAME", "rb") as f:
    f_content = f.read()
    content = ubinascii.hexlify(f_content)
print(content.decode('utf-8'))
"""
"""Print the content of a file present on the board (with format 2 hexadecimal digits per byte)"""

TESTFILE: str = """
import os
try:
    ret = os.stat('FILENAME')
    print(ret)
except Exception as ex:
    print(ex)
"""
"""Test if a file is present on the board"""

FILEINFOS: str = """
import os
def fileinfo(filename):
    f_info = []
    try:
        f_info.append(filename)
        f_info.append(os.stat(filename)[0])
        f_info.append(os.stat(filename)[1])
        f_info.append(os.stat(filename)[6])
    except Exception as ex:
        print(ex)
    return f_info
print(fileinfo("FILENAME"))
"""

FLASHFREESIZE: str = """
import os
statvfs = os.statvfs('/')
f_bsize, f_frsize, f_blocks,f_bfree,f_bavail, f_bavail, f_ffree, f_favail, f_flag, f_namemax=0,1,2,3,4,5,6,7,8,9
free_size = statvfs[f_frsize] * statvfs[f_bfree]
print(free_size)
"""
"""Return the free size of the flash"""

DELETE: str = """
import os
try:
    os.remove('FILENAME')
except Exception as ex:
    print(ex)
"""

DELETEDIR: str = """
import os
def rmvdir(dir):
    for i in os.ilistdir(dir):
        if i[1] == 0x4000:
            rmvdir('{}/{}'.format(dir, i[0]))
        elif i[1] == 0x8000:
            try:
                os.remove('{}/{}'.format(dir, i[0]))
            except Exception as ex:
                print(ex)
    os.rmdir(dir)
rmvdir('FILENAME')
"""
"""Delete a directory and all his content"""

MKDIR: str = """
import os
try:
    os.mkdir('DIRNAME')
except Exception as ex:
    print(ex)
"""

WRITE: str = """
import ubinascii

try:
    with open('FILENAME', 'wb') as f:
        f.write(ubinascii.unhexlify('CONTENT'))
except Exception as ex:
    print(ex)

"""