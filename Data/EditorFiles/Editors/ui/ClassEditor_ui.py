# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClassEditor.ui'
#
# Created: Sat Jan 15 13:08:43 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ClassEditor(object):
    def setupUi(self, ClassEditor):
        ClassEditor.setObjectName("ClassEditor")
        ClassEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ClassEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(ClassEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ClassEditor)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ClassEditor)
        QtCore.QMetaObject.connectSlotsByName(ClassEditor)

    def retranslateUi(self, ClassEditor):
        ClassEditor.setWindowTitle(QtGui.QApplication.translate("ClassEditor", "ClassEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ClassEditor", "Name:", None, QtGui.QApplication.UnicodeUTF8))

