# encoding:utf-8

from PyQt6.QtGui import QIcon

import src.constant as constant

def get_icon(icon_name):
    """The icon_name must be the same as the icon present in the assets/icons directory"""
    return QIcon("{}/{}.png".format(get_icon_path(), icon_name))

def get_icon_path():
    """Return the path where the icons are"""
    return "{}/assets/icons/".format(constant.MAIN_PATH)