# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WeaponEditor.ui'
#
# Created: Sat Sep 25 00:20:53 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_WeaponEditor(object):
    def setupUi(self, WeaponEditor):
        WeaponEditor.setObjectName("WeaponEditor")
        WeaponEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(WeaponEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(WeaponEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(WeaponEditor)
        self.name.setEnabled(True)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(WeaponEditor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(WeaponEditor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.type = QtGui.QLineEdit(WeaponEditor)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(WeaponEditor)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(WeaponEditor)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.subtype = QtGui.QComboBox(WeaponEditor)
        self.subtype.setEnabled(True)
        self.subtype.setEditable(False)
        self.subtype.setObjectName("subtype")
        self.gridLayout.addWidget(self.subtype, 5, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.damage0 = QtGui.QSpinBox(WeaponEditor)
        self.damage0.setMaximum(99)
        self.damage0.setObjectName("damage0")
        self.horizontalLayout.addWidget(self.damage0)
        self.label_6 = QtGui.QLabel(WeaponEditor)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.damage1 = QtGui.QSpinBox(WeaponEditor)
        self.damage1.setMaximum(999)
        self.damage1.setObjectName("damage1")
        self.horizontalLayout.addWidget(self.damage1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 2, 1, 1)
        self.label_7 = QtGui.QLabel(WeaponEditor)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cost = QtGui.QSpinBox(WeaponEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName("cost")
        self.horizontalLayout_2.addWidget(self.cost)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bonus = QtGui.QSpinBox(WeaponEditor)
        self.bonus.setObjectName("bonus")
        self.horizontalLayout_3.addWidget(self.bonus)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 7, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 85, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(WeaponEditor)
        QtCore.QMetaObject.connectSlotsByName(WeaponEditor)

    def retranslateUi(self, WeaponEditor):
        WeaponEditor.setWindowTitle(QtGui.QApplication.translate("WeaponEditor", "WeaponEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WeaponEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("WeaponEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("WeaponEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("WeaponEditor", "Subtype:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("WeaponEditor", "Damage:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("WeaponEditor", "d", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("WeaponEditor", "Bonus:", None, QtGui.QApplication.UnicodeUTF8))
