# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClassEditor.ui'
#
# Created: Sun Aug 21 00:52:04 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ClassEditor(object):
    def setupUi(self, ClassEditor):
        ClassEditor.setObjectName(_fromUtf8("ClassEditor"))
        ClassEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ClassEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ClassEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ClassEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ClassEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), ClassEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(ClassEditor)

    def retranslateUi(self, ClassEditor):
        ClassEditor.setWindowTitle(QtGui.QApplication.translate("ClassEditor", "ClassEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ClassEditor", "Name:", None, QtGui.QApplication.UnicodeUTF8))

