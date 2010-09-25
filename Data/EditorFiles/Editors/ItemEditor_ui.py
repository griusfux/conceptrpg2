# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ItemEditor.ui'
#
# Created: Sat Sep 25 00:20:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ItemEditor(object):
    def setupUi(self, ItemEditor):
        ItemEditor.setObjectName("ItemEditor")
        ItemEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ItemEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(ItemEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ItemEditor)
        self.name.setEnabled(True)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(ItemEditor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ItemEditor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.type = QtGui.QLineEdit(ItemEditor)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 3, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cost = QtGui.QSpinBox(ItemEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName("cost")
        self.horizontalLayout.addWidget(self.cost)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(ItemEditor)

    def retranslateUi(self, ItemEditor):
        ItemEditor.setWindowTitle(QtGui.QApplication.translate("ItemEditor", "ItemEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ItemEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ItemEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ItemEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))

