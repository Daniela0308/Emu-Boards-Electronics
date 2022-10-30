# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *

import QTermWidget

import view
import os
import subprocess
import settings

from pathlib import Path


class Editor(QWidget):
    def __init__(self):
        super(Editor, self).__init__()
        self.setting_editor = QSettings('EmuBoardsElectronics', 'Editor Settings')
        self.sci = QsciScintilla()
        self.sci.setUtf8(True)

        #Reading settings Tabs and indentation
        Guides = bool(int(self.setting_editor.value('Indentation_Guides')))
        self.sci.setIndentationGuides(Guides)
        Auto = bool(int(self.setting_editor.value('Auto_Indent')))
        self.sci.setAutoIndent(Auto)
        CareLine = bool(int(self.setting_editor.value('Care_Line_Visible')))
        self.sci.setCaretLineVisible(CareLine)
        TabWidth = int(self.setting_editor.value('Tab_Width'))
        self.sci.setTabWidth(TabWidth)
        Background = str(self.setting_editor.value('Care_Line_Background_Color'))
        self.sci.setCaretLineBackgroundColor(QColor(Background))

        #Reading settings font
        Font = str(self.setting_editor.value('Family_Font'))
        Size = int(self.setting_editor.value('Size_Font'))

        self.myFont = QFont()
        self.myFont.setFamily(Font)
        self.myFont.setPointSize(Size)
        self.sci.setFont(self.myFont)

        # 1. Text wrapping
        self.sci.setWrapMode(QsciScintilla.WrapCharacter)

        # 2. End-of-line mode
        self.sci.setEolMode(QsciScintilla.EolUnix)
        self.sci.setEolVisibility(False)

        # 5. Margins
        self.sci.setMarginType(1, QsciScintilla.NumberMargin)
        self.sci.setMarginWidth(2, "00")

        # 6. Lexer basics
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(self.myFont)
        self.sci.setLexer(self.lexer)

        grid = QGridLayout()
        grid.addWidget(self.sci, 2, 0)
        self.setLayout(grid)


class Simulation(QWidget):
    def __init__(self):
        super(Simulation, self).__init__()
        self.view = view.View()
        self.terminal = QTermWidget.QTermWidget()


        self.grid = QGridLayout()
        self.grid.addWidget(self.view, 0, 0)
        self.grid.addWidget(self.terminal, 1, 0, 2, 2)

        self.setLayout(self.grid)


class Workspace(QWidget):
    def __init__(self):
        super(Workspace, self).__init__()
        self.editor = Editor()
        self.simulation = Simulation()

        self.widget = QWidget()
        self.stacked_layout = QStackedLayout()
        self.widget.setLayout(self.stacked_layout)
        self.stacked_layout.addWidget(self.simulation)
        self.stacked_layout.addWidget(self.editor)


    def options(self, arr_opt):
        self.setting_editor = QSettings('EmuBoardsElectronics', 'Editor Settings')

        #Settings Tabs and indentation
        self.editor.sci.setIndentationGuides(arr_opt[0])
        self.setting_editor.setValue('Indentation_Guides', int(arr_opt[0]))
        self.editor.sci.setAutoIndent(arr_opt[1])
        self.setting_editor.setValue('Auto_Indent', int(arr_opt[1]))
        self.editor.sci.setTabWidth(arr_opt[2])
        self.setting_editor.setValue('Tab_Width', int(arr_opt[2]))
        self.editor.sci.setCaretLineVisible(arr_opt[5])
        self.setting_editor.setValue('Care_Line_Visible', int(arr_opt[5]))
        self.editor.sci.setCaretLineBackgroundColor(QColor(arr_opt[6]))
        self.setting_editor.setValue('Care_Line_Background_Color', (arr_opt[6]))

        #Settings Font
        self.myFont = QFont()
        self.myFont.setFamily(arr_opt[3])
        self.setting_editor.setValue('Family_Font', arr_opt[3])
        self.myFont.setPointSize(arr_opt[4])
        self.setting_editor.setValue('Size_Font', int(arr_opt[4]))
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(self.myFont)
        self.editor.sci.setLexer(self.lexer)


    def setComponent(self, image, name, posX, posY):
        self.simulation.view.setComponent(image, name, posX, posY)

    def createOpenItems(self, image, name, posX, posY):
        self.simulation.view.createOpenItems(image, name, posX, posY)

    def clear(self):
        self.simulation.view.clear()

    def elementsCreated(self):
        return self.simulation.view.elementsCreated()
