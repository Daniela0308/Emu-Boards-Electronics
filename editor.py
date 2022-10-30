# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.Qsci import *
from PyQt5.QtGui import *


class Editor(QsciScintilla):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setUtf8(True)
        self.myFont = QFont()
        self.setFont(self.myFont)

        self.myFont.setPointSize(12)

        # 1. Text wrapping
        self.setWrapMode(QsciScintilla.WrapCharacter)

        # 2. End-of-line mode
        self.setEolMode(QsciScintilla.EolUnix)
        self.setEolVisibility(False)

         # 3. Indentation

        #elf.setTabWidth(8)
        #self.setIndentationGuides(val)
        #self.setAutoIndent(True)

        # 4. Caret
        self.setCaretLineVisible(False)
        self.setCaretLineBackgroundColor(QColor("#f5f55d"))
        self.setCaretWidth(100)

        # 5. Margins
        self.setMarginType(1, QsciScintilla.NumberMargin)
        self.setMarginWidth(2, "00")

        # 6. Lexer basics
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(self.myFont)
        self.setLexer(self.lexer)

        # 7. Autocompletion


