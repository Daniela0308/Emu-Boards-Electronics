# This Python file uses the following encoding: utf-8
import sys
import os

import resource

from PySide2.QtSvg import QGraphicsSvgItem
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsSceneMouseEvent, QWidget, QGraphicsRectItem
from PySide2.QtCore import QFile, Qt, QCoreApplication, QProcess, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QColor, QBrush

from multiprocessing import shared_memory

DISPLAY_BLANK               = 0x00
NORMAL_MODE                 = 0x10
ALL_DISPLAY_SEGMENTS_ON     = 0x01
INVERSE_VIDEO_MODE          = 0x11

class raspi(QMainWindow):
    def __init__(self):
        super(raspi, self).__init__()
        self.load_ui()

        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionStop.triggered.connect(self.stop)
        self.ui.actionLCD.triggered.connect(self.lcd)
        self.ui.actionRaspberry_Pi.triggered.connect(self.raspberry)
        self.ui.actionLed.triggered.connect(self.led)
        self.ui.actionButton.triggered.connect(self.button)


        self.process = QProcess()
        self.time = QTimer()

        self.process.setProgram('/home/daniela/Documentos/qemu/qemu-system-aarch64')
        list = ['-m', '1024', '-M', 'raspi3', '-kernel', '/home/daniela/Documentos/qemu/kernel8.img', '-dtb',
        '/home/daniela/Documentos/qemu/bcm2710-rpi-3-b-plus.dtb', '-sd',
        '/home/daniela/Documentos/qemu/2020-08-20-raspios-buster-armhf.img',
        '-append', 'console=ttyAMA0 root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4',
        '-vnc', ':0', '-device', 'usb-tablet', '-device', 'usb-kbd', '-L',
        '/home/daniela/Documentos/qemu/pc-bios', '-nographic', '-device',
        'usb-net,netdev=net0', '-netdev', 'user,id=net0,hostfwd=tcp::5555-:22']

        self.process.setArguments(list)
        self.process.readyReadStandardError.connect(self.read)
        self.process.readyReadStandardOutput.connect(self.read)

        self.time.timeout.connect(self.timer)
        self.time.start(30)

        self.scene = Scene()
        self.ui.graphicsView.setScene(self.scene)

        self.shm = shared_memory.SharedMemory(name = "QEMUShm", create = True, size = 4)

        self.ui.showMaximized()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def read(self):
        try:
            lec = str(self.process.readAll(), 'utf-8')
            self.ui.plainTextEdit.appendPlainText(lec)
        except ValueError:
            pass

    def run(self):
        self.process.start()
        ret = self.process.waitForStarted(2000)
        print(ret)

    def stop(self):
        self.process.terminate()
        ret = self.process.waitForFinished(2000)
        print(ret)

    def lcd(self):
        self.scene.setComponent('Lcd')

    def raspberry(self):
        self.scene.setComponent('Raspberry')

    def led(self):
        self.scene.setComponent('Led')

    def button(self):
        self.scene.setComponent('Button')

    def timer(self):
        y = self.shm.buf.tobytes()
        value = int.from_bytes(y, 'little')
        self.scene.modeLCD(value)
        print(value)

        for i in range (32):
            if(value & (1 << i)):
                print('Conectado al pin: ', i)


        if(value != 0):
            state = True
        else:
            state = False
        self.scene.alternate(state)

        if(self.scene.button or not(self.scene.button)):
            self.write()

    def write(self):
        if (self.scene.button):
            value = 1
        else:
            value = 0

        self.shm.buf[:4] = value.to_bytes(4, 'little')

    def __del__(self):
        self.shm.close()
        self.shm.unlink()

class Scene(QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.item_lcd = QGraphicsSvgItem(":/new/nokia.svg")
        self.item_lcd.hide()
        self.addItem(self.item_lcd)

        self.item_raspi = QGraphicsSvgItem(":/new/raspberrypi.svg")

        self.item_led_on = QGraphicsSvgItem(":/new/ledon.svg")
        self.item_led_on.hide()
        self.item_led_off = QGraphicsSvgItem(":/new/ledoff.svg")

        self.item_button_on = QGraphicsSvgItem(":/new/buttonon.svg")
        self.item_button_on.hide()
        self.item_button_off = QGraphicsSvgItem(":/new/buttonoff.svg")

        self.component = None
        self.button = False
        self.count = 1

        self.lcd = LCD(super(), self.item_lcd)

    def modeLCD(self, value):
        self.value = value
        self.lcd.modeScreen(self.value)
        print(self.value)

    def setComponent(self, component):
        self.component = component

    def mousePressEvent(self, event):
        if(self.component == 'Lcd'):
           self.addItem(self.item_lcd)

        elif(self.component == 'Raspberry'):
            self.addItem(self.item_raspi)

        elif(self.component == 'Led'):
            self.addItem(self.item_led_on)
            self.addItem(self.item_led_off)

        elif(self.component == 'Button'):
            self.addItem(self.item_button_on)
            self.addItem(self.item_button_off)

        super(Scene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if(self.component == 'Lcd'):
            self.item_lcd.setPos(event.scenePos())
            self.lcd.constructor()
            self.lcd.update()
            #self.component = None
            self.item_lcd.show()

        elif(self.component == 'Raspberry'):
            self.item_raspi.setPos(event.scenePos())
            #self.component = None

        elif(self.component == 'Led'):
            self.item_led_off.setPos(event.scenePos())
            self.item_led_on.setPos(event.scenePos())
            #self.component = None

        elif(self.component == 'Button'):
            self.item_button_on.setPos(event.scenePos())
            self.item_button_off.setPos(event.scenePos())
            self.component = None

        elif(event.scenePos().x() > self.item_button_off.pos().x() and event.scenePos().x() < self.item_button_off.pos().x()+45):
            if(event.scenePos().y() > self.item_button_off.pos().y() and event.scenePos().y() < self.item_button_off.pos().y()+20):
                if(self.count%2 == 1):
                    self.button = True
                    self.item_button_on.show()
                    self.item_button_off.hide()
                    print('ON')
                elif(self.count%2 == 0):
                    self.button = False
                    self.item_button_on.hide()
                    self.item_button_off.show()
                    print('OFF')
                self.count = self.count + 1

        super(Scene, self).mouseReleaseEvent(event)

    def alternate(self, state):
        if(state):
            self.item_led_on.show()
            self.item_led_off.hide()
        else:
            self.item_led_off.show()
            self.item_led_on.hide()


class LCD(QWidget):
    def __init__(self, scene_lcd, item):
        super(LCD, self).__init__()

        self.scene = scene_lcd
        self.item = item

        self.colum = 0
        self.row = 0
        self.configuration = 0

        self.size = 1.5
        self.getXmin = self.item.x()
        self.getXmax = self.item.boundingRect().width()-self.size
        self.getYmin = self.item.y()
        self.getYmax = self.item.boundingRect().height()-self.size

        self.PosyX = (self.getXmax/2.0) - 42*self.size + self.colum*self.size
        self.PosyY = self.getYmin + 30*self.size + 8*self.row*self.size

        self.rects = []
        i = 0
        j = 0

        for b in range(48):
            for c in range(84):
                self.rects.append(self.scene.addRect(self.PosyX+i, self.PosyY+j, self.size, self.size))
                self.rects[c+b*84].hide()
                self.rects[c+b*84].setBrush(QBrush(QColor(80, 89, 72)))
                self.rects[c+b*84].setPen(Qt.NoPen)
                i += self.size
            j += self.size
            i = 0

    def constructor(self):
        self.DisplayControl(NORMAL_MODE)
        self.setPosy(2, 0)
        self.write(0x7f)
        self.write(0x40)
        self.write(0x40)
        self.write(0x40)
        self.write(0x40)
        self.setPosy(2, 2)
        self.write(0x7f)
        self.write(0x41)
        self.write(0x41)
        self.write(0x22)
        self.write(0x1c)
        self.setPosy(2, 4)
        self.write(0x7e)
        self.write(0x11)
        self.write(0x11)
        self.write(0x11)
        self.write(0x7e)

    def write(self, data):
        count = self.row*8
        if self.configuration == NORMAL_MODE:
            for y in range(8):
                if data & (1 << y):
                   self.rects[count*84+self.colum].setBrush(Qt.white)
                   self.rects[count*84+self.colum].setPen(Qt.NoPen)
                   self.rects[count*84+self.colum].show()
                   self.aux= count*84+self.colum
                elif not data & (1 << y):
                    self.rects[count*84+self.colum].setBrush(QBrush(QColor(80, 89, 72)))
                    self.rects[count*84+self.colum].setPen(Qt.NoPen)
                    self.rects[count*84+self.colum].show()
                    self.aux= count*84+self.colum
                count += 1

        elif self.configuration == INVERSE_VIDEO_MODE:
            for y in range(8):
                if not data & (1 << y):
                    self.rects[count*84+self.colum].setBrush(Qt.white)
                    self.rects[count*84+self.colum].setPen(Qt.NoPen)
                    self.rects[count*84+self.colum].show()
                elif data & (1 << y):
                    self.rects[count*84+self.colum].setBrush(QBrush(QColor(80, 89, 72)))
                    self.rects[count*84+self.colum].setPen(Qt.NoPen)
                    self.rects[count*84+self.colum].show()
                count += 1

        self.colum += 1
        if self.colum > 83:
            self.row += 1
            self.colum = 0
            if self.row > 5:
                self.row= 0

    def setPosy(self, NewColum, NewRow):
        if NewColum > 83:
            NewColum = 83
        if NewRow > 5:
            NewRow = 5

        self.colum = NewColum
        self.row = NewRow

    def DisplayControl(self, mode):
        self.configuration = NORMAL_MODE

        if mode == DISPLAY_BLANK:
            for i in range(504):
                self.write(0x00)
        elif mode == ALL_DISPLAY_SEGMENTS_ON:
            for i in range(504):
                self.write(0xff)
        elif mode == INVERSE_VIDEO_MODE:
            for i in range(504):
                self.write(0xff)

        self.configuration = mode

    def update(self):
        for b in range(48):
            for c in range(84):
                self.rects[c+b*84].setPos(self.item.x(), self.item.y())

    def modeScreen(self, screen):
        self.screen = screen
        print(self.screen)
        if((self.screen & (0x30))== 0x30):
            self.DisplayControl(NORMAL_MODE)
            for i in range(504):
                self.write(0x00)
            self.setPosy(2, 0)
            self.write(0x7f)
            self.write(0x40)
            self.write(0x40)
            self.write(0x40)
            self.write(0x40)
            self.setPosy(2, 2)
            self.write(0x7f)
            self.write(0x41)
            self.write(0x41)
            self.write(0x22)
            self.write(0x1c)
            self.setPosy(2, 4)
            self.write(0x7e)
            self.write(0x11)
            self.write(0x11)
            self.write(0x11)
            self.write(0x7e)
        elif((self.screen & (0x20))== 0x20):
            self.DisplayControl(INVERSE_VIDEO_MODE)
            self.setPosy(2, 0)
            self.write(0x7f)
            self.write(0x40)
            self.write(0x40)
            self.write(0x40)
            self.write(0x40)
            self.setPosy(2, 2)
            self.write(0x7f)
            self.write(0x41)
            self.write(0x41)
            self.write(0x22)
            self.write(0x1c)
            self.setPosy(2, 4)
            self.write(0x7e)
            self.write(0x11)
            self.write(0x11)
            self.write(0x11)
            self.write(0x7e)
        elif((self.screen & (0x10))== 0x10):
            self.DisplayControl(ALL_DISPLAY_SEGMENTS_ON)
        elif((self.screen & (0x08))== 0x08):
            self.DisplayControl(DISPLAY_BLANK)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = raspi()
    sys.exit(app.exec_())
