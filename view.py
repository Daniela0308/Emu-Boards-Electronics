import json

from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class View(QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        self.element = None
        self.scene = Scene()
        self.setMouseTracking(True)
        self.setScene(self.scene)

    def setComponent(self, image, name, posX, posY):
        self.scene.setComponent(image, name, posX, posY)

    def createOpenItems(self, image, name, posX, posY):
        self.scene.setComponent(image, name, posX, posY)
        self.scene.createItem()
        #self.scene.setPos(posX, posY)
        self.setScene(self.scene)

    def createItem(self):
        self.scene.createItem()

    def clear(self):
        self.scene.clear()

    def mousePressEvent(self, event):
        self.scene.createItem()
        self.element = self.scene.itemAt(self.mapToScene(event.pos()) , QTransform())

        super(View, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.element = None
        super(View, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.element is not None:
            self.element.setPos(self.mapToScene(event.pos()))

        elif(self.scene.itemAt(self.mapToScene(event.pos()), QTransform())):
            self.comp = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())

            #self.dataJson = self.scene.elementsCreated()
            #for comp in  range(len(self.dataJson)):
             #   if(self.dataJson[comp][0]['item'] == self.scene.itemAt(self.mapToScene(event.pos()), QTransform())):
              #      self.dataJson[comp][0]['posX']= 4
               #     self.dataJson[comp][0]['posY']= 6

        super(View, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.scene.removeItem(self.comp)
        super(View, self).keyPressEvent(event)

    def elementsCreated(self):
        return self.scene.elementsCreated()

class Scene(QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.items = {}
        self.elements = []
        self.dataJson = {}
        self.element = None


    def setComponent(self, image, name, posX, posY):
        self.name = name
        self.comp = image
        self.posX = posX
        self.posY = posY
        self.value = True

    def createItem(self):
        if(self.value):
            if self.name not in self.items:
                self.items[self.name] = []
            else:
                pass

            self.items[self.name].append(QGraphicsSvgItem(self.comp))

            if self.posX == None and self.posY == None:
                self.addItem(self.items[self.name][-1])
                self.toolTip = self.name + str(len(self.items[self.name])-1)
                self.items[self.name][-1].setToolTip(self.toolTip)

            else:
                self.items[self.name][-1].setPos(self.posX, self.posY)
                self.addItem(self.items[self.name][-1])
                self.toolTip = self.name + str(len(self.items[self.name])-1)
                self.items[self.name][-1].setToolTip(self.toolTip)

            for i in self.items[self.name]:
                self.elements.append(i)


            self.dataJson[self.toolTip] = []
            self.dataJson[self.toolTip].append({
            'name' : self.name,
            'item' : str(self.items[self.name][0]),
            'route_image' : self.comp,
            'posX' : 0,
            'posY' : 0
            })


    def clear(self):
        for e in self.elements:
            self.removeItem(e)

        self.elements.clear()

    def mousePressEvent(self, event):
        print(self.elements)
        self.element = self.itemAt(event.scenePos(), QTransform())

        super(Scene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.value = False
        self.element = None

        if(self.itemAt(event.scenePos(), QTransform())):
            self.com = self.itemAt(event.scenePos(), QTransform())

            for comp in self.dataJson:
                self.dataJson[self.toolTip][0]['posX'] = self.com.pos().x()
                self.dataJson[self.toolTip][0]['posY'] = self.com.pos().y()


        super(Scene, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.element is not None:
            self.element.setPos(event.scenePos())

        elif(self.itemAt(event.scenePos(), QTransform())):
            self.com = self.itemAt(event.scenePos(), QTransform())



        super(Scene, self).mouseMoveEvent(event)

    def elementsCreated(self):
        return self.dataJson
