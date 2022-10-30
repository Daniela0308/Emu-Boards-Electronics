# This Python file uses the following encoding: utf-8
import os
from importlib.machinery import SourceFileLoader


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ComponentsFunctions:
    def __init__(self):
        self.address = os.path.dirname(os.path.abspath(__file__)) + '/components'
        components = os.listdir(self.address)

    def components_read(self, comp):
        self.comp = comp
        address_file = self.address + '/' + self.comp

        for file in os.listdir(address_file):
           if file.endswith(".py"):
               self.adr = address_file + "/" + file
               self.file = SourceFileLoader('file', self.adr).load_module()


    def emu_start(self):
        self.file.start()

    def emu_stop(self):
        self.file.stop()
