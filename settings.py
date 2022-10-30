# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import editor
import workspace

class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.workspace = workspace.Workspace()

        self.identation()
        self.font()
        self.setWindowTitle("Editor Settings")

        # creamos un layout y lo establecemos en el widget
        rootLayout = QVBoxLayout()
        layout = QHBoxLayout()

        # creamos unos botones predeterminados
        self.btnCancel = QPushButton(QIcon(":/Resource/cancelar.png"), "Cancel", self)
        self.btnApply = QPushButton(QIcon(":/Resource/aceptar.png"), "Apply", self)
        self.btnCancel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnApply.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # y los añadimos al layout
        layout.addWidget(self.btnCancel)
        layout.addWidget(self.btnApply)

        rootLayout.addWidget(self.identationGroupBox)
        rootLayout.addWidget(self.fontGroupBox)
        rootLayout.addLayout(layout)

        self.setLayout(rootLayout)

        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)


    def identation(self):
        self.setting_editor = QSettings('EmuBoardsElectronics', 'Editor Settings')
        if self.setting_editor.value('Indentation_Guides', None) is None:
            self.setting_editor.setValue('Indentation_Guides', 0)
            Guides = False
        elif self.setting_editor.value('Auto_Indent', None) is None:
            self.setting_editor.setValue('Auto_Indent', 0)
            Auto = False
        elif self.setting_editor.value('Tab_Width', None) is None:
            self.setting_editor.setValue('Tab_Width', 4)
            TabWidth = 4
        elif self.setting_editor.value('Care_Line_Visible', None) is None:
            self.setting_editor.setValue('Care_Line_Visible', 0)
            CareLine = False
        elif self.setting_editor.value('Care_Line_Background_Color', None) is None:
            self.setting_editor.setValue('Care_Line_Background_Color', 'darkBlue')
            Background = 'darkBlue'
        else:
            Guides = bool(int(self.setting_editor.value('Indentation_Guides')))
            Auto = bool(int(self.setting_editor.value('Auto_Indent')))
            CareLine = bool(int(self.setting_editor.value('Care_Line_Visible')))
            TabWidth = int(self.setting_editor.value('Tab_Width'))
            Background = self.setting_editor.value('Care_Line_Background_Color')

        self.identationGroupBox = QGroupBox("Tabs and indentation")
        formLayout = QFormLayout()

        color = ['darkBlue', 'darkCyan', 'darkGreen', 'darkGray', 'darkMagenta', 'darkRed']

        self.setIndentationGuides = QCheckBox()
        self.setIndentationGuides.setChecked(Guides)
        self.setAutoIndent = QCheckBox()
        self.setAutoIndent.setChecked(Auto)
        self.setCareLineVisible = QCheckBox()
        self.setCareLineVisible.setChecked(CareLine)
        self.setTabWidth = QSpinBox()
        self.setTabWidth.setValue(TabWidth)
        self.colorLine = QComboBox()
        self.colorLine.addItems(color)
        self.colorLine.setCurrentText(Background)

        formLayout.addRow("Indentation Guides:", self.setIndentationGuides)
        formLayout.addRow("Auto Indentation:", self.setAutoIndent)
        formLayout.addRow("Care Line Visible:", self.setCareLineVisible)
        formLayout.addRow("Tab Width:", self.setTabWidth)
        formLayout.addRow("Color line visible :", self.colorLine)

        self.identationGroupBox.setLayout(formLayout)


    def font(self):
        self.fontGroupBox = QGroupBox("Font")
        formLayout = QFormLayout()

        self.setting_editor = QSettings('EmuBoardsElectronics', 'Editor Settings')
        if self.setting_editor.value('Family_Font', None) is None:
            self.setting_editor.setValue('Family_Font', 'Arial')
            Font = 'Arial'
        elif self.setting_editor.value('Size_Font', None) is None:
            self.setting_editor.setValue('Size_Font', 12)
            Size = 12
        else:
            Font = str(self.setting_editor.value('Family_Font'))
            Size = int(self.setting_editor.value('Size_Font'))

        family = ['Arial', 'AnyStyle', 'Courier', 'Cursive', 'Decorative', 'Fantasy', 'Times', 'System']

        self.familyFont = QComboBox()
        self.familyFont.addItems(family)
        self.familyFont.setCurrentText(Font)
        self.sizeFont = QSpinBox()
        self.sizeFont.setValue(Size)

        formLayout.addRow("Family:", self.familyFont)
        formLayout.addRow("Size:", self.sizeFont)

        self.fontGroupBox.setLayout(formLayout)


    def getResults(self):
        if QDialog.Accepted:
            opt = []
            opt.append(self.setIndentationGuides.isChecked())
            opt.append(self.setAutoIndent.isChecked())
            opt.append(self.setTabWidth.value())
            opt.append(self.familyFont.currentText())
            opt.append(self.sizeFont.value())
            opt.append(self.setCareLineVisible.isChecked())
            opt.append(self.colorLine.currentText())

            return opt
        else:
            return None

