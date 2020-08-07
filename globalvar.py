# -*- coding: utf-8 -*-
import os
import sys


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


USER_HOME = os.path.expanduser('~')
ROOT_DIR = os.path.join(USER_HOME, "DSTServerManager")
CONFIG_DIR = resource_path("Configs")
CLUSTER_DIR = os.path.join(ROOT_DIR, "Clusters")
TEMP_FILE = os.path.join(CONFIG_DIR, "temp.ini")
