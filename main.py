# This Python file uses the following encoding: utf-8
import sys
import os

import resources
import components
import view
import workspace
import settings
import componentsFunctions

import json

from pathlib import Path

import QTermWidget


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic


class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.load_ui()
        self.setWindowTitle("EmuBoardsElectronics")


        #Create Objects
        self.process = QProcess()
        self.scene = view.Scene()
        self.settings = settings.Settings()
        self.workspace = workspace.Workspace()


        self.comp_function = componentsFunctions.ComponentsFunctions()
        self.comp = components.Components()
        self.component = self.comp.jsonList

        #Actions
        self.actionExit.triggered.connect(self.window_close)
        self.actionChange.triggered.connect(self.windowChange)
        self.actionEditor.triggered.connect(self.editorSettings)

        self.actionOpen.triggered.connect(self.openProject)
        self.actionSave.triggered.connect(self.saveProject)
        self.actionNew.triggered.connect(self.newProject)

        self.actionzoomPlus.triggered.connect(self.zoomPlus)
        self.actionRun.triggered.connect(self.run)
        self.actionStop.triggered.connect(self.stop)

        self.settings.btnCancel.clicked.connect(self.cancel)
        self.settings.btnApply.clicked.connect(self.apply)


        self.createToolMenu()


        #Add class
        self.ui.graphic.addWidget(self.workspace.widget)
        self.ui.toolBar_editor.setVisible(False)
        self.ui.showMaximized()


    def newProject(self):
        msgbox = QMessageBox.question(self,"Warning","Do you want to save this project before creating a new project?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msgbox == QMessageBox.Yes:
            self.workspace.clear()
        else:
            self.saveProject()
            self.workspace.clear()


    def openProject(self):
        file = QFileDialog.getOpenFileName(self, 'Open Porject', str(Path.home()), 'Project File (*.ebe*)')
        self.workspace.clear()

        if file[0]:
            with open(file[0], 'rt') as f:
                data = json.load(f)

        for f in data:
            #self.workspace.clear()
            self.workspace.createOpenItems(data[f][0]['route_image'], data[f][0]['name'], data[f][0]['posX'], data[f][0]['posY'])

    def saveProject(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file, _ = QFileDialog.getSaveFileName(self, 'Save Project', str(Path.home()), 'Project File (*.ebe*)', options=options)

        with open(file, 'w') as f:
            json.dump(self.workspace.elementsCreated(), f, indent = 4)


    def run(self):
        self.comp_function.components_read('raspberry')
        print(self.comp_function.emu_start())


    def stop(self):
        self.comp_function.components_read('raspberry')
        print(self.comp_function.emu_stop())

    def zoomPlus(self):
        print(self.workspace.elementsCreated())

    def apply(self):
        opt = self.settings.getResults()
        self.workspace.options(opt)
        self.settings.close()

    def cancel(self):
        self.settings.close()

    def editorSettings(self):
        self.settings.exec_()

    def createToolMenu(self):
        category = []
        for comp in self.component:
            if not self.component[comp]['category'] in category:
                category.append(self.component[comp]['category'])
                subMenu = self.menuComponents.addMenu(self.component[comp]['category'])
            action = QAction(QIcon(self.component[comp]['fullPath'] + "/" + self.component[comp]['image']), self.component[comp]['name'], self)
            subMenu.addAction(action)
            action.triggered.connect(self.action)

    def windowChange(self):
        name = self.sender().text()
        self.setWindowTitle(name)
        if(name == 'Editor'):
            self.actionChange.setText('Simulation')
            self.workspace.stacked_layout.setCurrentIndex(1)
            self.ui.toolBar.setVisible(False)
            self.ui.toolBar_editor.setVisible(True)

        if(name == 'Simulation'):
            self.actionChange.setText('Editor')
            self.workspace.stacked_layout.setCurrentIndex(0)
            self.ui.toolBar.setVisible(True)
            self.ui.toolBar_editor.setVisible(False)

    def action(self):
        componentSelected = self.sender().text()
        self.workspace.setComponent(self.component[componentSelected]['fullPath'] + "/" + self.component[componentSelected]['image'], self.component[componentSelected]['name'], None, None)

    def window_close(self, event):
        msgbox = QMessageBox.question(self,"Warning","Are you sure to close the aplication?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msgbox == QMessageBox.Yes:
            self.close()
        else:
            event.ignore()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = uic.loadUi(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = main()
    sys.exit(app.exec_())


