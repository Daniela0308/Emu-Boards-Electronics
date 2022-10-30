# This Python file uses the following encoding: utf-8

import os
import view


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Components():
    def __init__(self):
        self.jsonList = {}

        address = os.path.dirname(os.path.abspath(__file__)) + '/components'
        components = os.listdir(address)

        for i in range(len(components)):
            address_file = address + '/' + components[i]

            for file in os.listdir(address_file):
                if file.endswith(".json"):
                    jsonList = self.readJson(address_file + "/" + file)                    
                    self.jsonList[jsonList['name']] = jsonList
                    self.jsonList[jsonList['name']]['fullPath'] = address_file


    def readJson(self, address):
        address = address
        jsonList = {}

        #Open file
        file = QFile()
        file.setFileName(address)
        file.open(QIODevice.ReadOnly | QIODevice.Text)
        val = file.readAll()
        file.close()

        document = QJsonDocument.fromJson(val)

        #Name
        object_name = document.object()
        name = object_name["name"].toString()
        jsonList['name'] = name

        #Category
        object_category = document.object()
        category = object_category["category"].toString()
        jsonList['category'] = category

        #Image
        object_image= document.object()
        image = object_image["image"].toString()
        jsonList['image'] = image

        #Code_Funtions
        object_code_functions= document.object()
        code_functions = object_code_functions["code_functions"].toString()
        jsonList['code_functions'] = code_functions

        #State
        object_state = document.object()
        value_state = object_state["state"]
        item_state = value_state.toObject()
        jsonList['state'] = {key:value.toString() for (key, value) in item_state.items()}

        #connections
        object_connections = document.object()
        value_connections = object_connections["connections"].toArray()
        jsonList['connections'] = {}

        for i in range(value_connections.__len__()):
            subobj_connections = value_connections[i].toObject()
            value_type = subobj_connections["type"].toString()
            value_coordinates = subobj_connections["coordinates"].toObject()

            jsonList['connections'][value_type] = {key:value.toString() for (key, value) in value_coordinates.items()}
            #dictionary comprehension, list comprehension

        return jsonList





