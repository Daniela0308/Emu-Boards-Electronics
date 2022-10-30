# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Holi(QWidget):
    def __init__(self):
        super(Holi, self).__init__()
        self.pix = QPixmap() # instanciar un objeto QPixmap
        self.lastPoint = QPoint() # punto de inicio
        self.endPoint = QPoint() # punto final
        self.initUi()

    def initUi(self):
         # El tamaño de la ventana se establece en 600 * 500
        self.resize(600, 500)
         # El tamaño del lienzo es 400 * 400, el fondo es blanco
        self.pix = QPixmap(400, 400)
        self.pix.fill(Qt.white)

     # La función de copia repintada se dibuja principalmente aquí
    def paintEvent(self,event):
        pp = QPainter(self.pix)
         # Dibuja una línea recta de acuerdo con las dos posiciones antes y después del puntero del mouse
        pp.drawLine(self.lastPoint, self.endPoint)
         # Hacer que el valor de la coordenada anterior sea igual al siguiente valor de la coordenada,
         # De esta manera, se puede dibujar una línea continua
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix) #Dibujar en el lienzo

    # Evento de prensa del ratón
    def mousePressEvent(self, event) :
             # Presione el botón izquierdo del mouse
        if event.button() == Qt.LeftButton :
                self.lastPoint = event.pos()
                self.endPoint = self.lastPoint

     # Evento de movimiento del mouse
    def mouseMoveEvent(self, event):
             # Mueva el mouse mientras presiona el botón izquierdo del mouse
        if event.buttons() and Qt.LeftButton :
                self.endPoint = event.pos()
                 #Hacer repintar
                self.update()

     # Evento de lanzamiento del mouse
    def mouseReleaseEvent( self, event):
             # Liberación del botón izquierdo del mouse
        if event.button() == Qt.LeftButton :
                self.endPoint = event.pos()
                 #Hacer repintar
                self.update()

