# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArmorEditor.ui'
#
# Created: Sat Sep 25 21:33:07 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ArmorEditor(object):
    def setupUi(self, ArmorEditor):
        ArmorEditor.setObjectName("ArmorEditor")
        ArmorEditor.setEnabled(True)
        ArmorEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ArmorEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(ArmorEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ArmorEditor)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(ArmorEditor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ArmorEditor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.type = QtGui.QLineEdit(ArmorEditor)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 2, 3, 1, 1)
        self.label_4 = QtGui.QLabel(ArmorEditor)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(ArmorEditor)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.subtype = QtGui.QComboBox(ArmorEditor)
        self.subtype.setEditable(False)
        self.subtype.setObjectName("subtype")
        self.gridLayout.addWidget(self.subtype, 5, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ac = QtGui.QSpinBox(ArmorEditor)
        self.ac.setMaximum(9999)
        self.ac.setObjectName("ac")
        self.horizontalLayout.addWidget(self.ac)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 3, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cost = QtGui.QSpinBox(ArmorEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName("cost")
        self.horizontalLayout_2.addWidget(self.cost)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(ArmorEditor)
        QtCore.QMetaObject.connectSlotsByName(ArmorEditor)
        ArmorEditor.setTabOrder(self.name, self.cost)
        ArmorEditor.setTabOrder(self.cost, self.type)
        ArmorEditor.setTabOrder(self.type, self.subtype)
        ArmorEditor.setTabOrder(self.subtype, self.ac)

    def retranslateUi(self, ArmorEditor):
        ArmorEditor.setWindowTitle(QtGui.QApplication.translate("ArmorEditor", "ArmorEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ArmorEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ArmorEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ArmorEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ArmorEditor", "Subtype:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ArmorEditor", "AC:", None, QtGui.QApplication.UnicodeUTF8))

