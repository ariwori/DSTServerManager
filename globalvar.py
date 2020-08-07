# -*- coding: utf-8 -*-
import os

USER_HOME = os.path.expanduser('~')
ROOT_DIR = os.path.join(USER_HOME, "DSTServerManager")
CONFIG_DIR = os.path.join(ROOT_DIR, "Configs")
CLUSTER_DIR = os.path.join(ROOT_DIR, "Clusters")
TEMP_FILE = os.path.join(CONFIG_DIR, "temp.ini")
