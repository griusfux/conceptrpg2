# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PowerEditor.ui'
#
# Created: Thu Jan 20 23:00:48 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PowerEditor(object):
    def setupUi(self, PowerEditor):
        PowerEditor.setObjectName("PowerEditor")
        PowerEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PowerEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtGui.QLineEdit(PowerEditor)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label = QtGui.QLabel(PowerEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.range_size = QtGui.QSpinBox(PowerEditor)
        self.range_size.setObjectName("range_size")
        self.horizontalLayout.addWidget(self.range_size)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PowerEditor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(PowerEditor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.range_type = QtGui.QComboBox(PowerEditor)
        self.range_type.setObjectName("range_type")
        self.gridLayout.addWidget(self.range_type, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(PowerEditor)
        QtCore.QMetaObject.connectSlotsByName(PowerEditor)

    def retranslateUi(self, PowerEditor):
        PowerEditor.setWindowTitle(QtGui.QApplication.translate("PowerEditor", "PowerEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PowerEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PowerEditor", "Range Size: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PowerEditor", "Range Type: ", None, QtGui.QApplication.UnicodeUTF8))

