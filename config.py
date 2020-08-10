# -*- coding: utf-8 -*-
import os
import configparser


class GlobalConfig(object):

    def __init__(self, config_file):
        self._config_file = config_file
        self._config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            file = open(config_file, 'w', encoding="utf-8")
            file.close()
        self._config.read(self._config_file, encoding='utf-8')

    def has_section(self, section):
        return self._config.has_section(section)

    def add_section(self, section):
        self._config.add_section(section)

    def get(self, section, name, strip_blank=True, strip_quote=True):
        s = self._config.get(section, name)
        if strip_blank:
            s = s.strip()
        if strip_quote:
            s = s.strip('"').strip("'")
        return s

    def set(self, section, key, value, strip_blank=True, strip_quote=True):
        if strip_blank:
            value = value.strip()
        if strip_quote:
            value = value.strip('"').strip("'")
        self._config.set(section, key, value)

    def setboolean(self, section, key, value):
        if value:
            value = "true"
        else:
            value = "false"
        self._config.set(section, key, value)

    def save(self, savefile):
        try:
            self._config.write(open(savefile, "w", encoding="utf-8"))
        except ImportError:
            pass

    def getboolean(self, section, name):
        return self._config.getboolean(section, name)
