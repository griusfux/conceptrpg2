# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArmorEditor.ui'
#
# Created: Fri Jun 17 22:12:32 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ArmorEditor(object):
    def setupUi(self, ArmorEditor):
        ArmorEditor.setObjectName(_fromUtf8("ArmorEditor"))
        ArmorEditor.setEnabled(True)
        ArmorEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ArmorEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ArmorEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ArmorEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(ArmorEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(ArmorEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(ArmorEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.type = QtGui.QComboBox(ArmorEditor)
        self.type.setEditable(False)
        self.type.setObjectName(_fromUtf8("type"))
        self.gridLayout.addWidget(self.type, 4, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.arcane_defense = QtGui.QSpinBox(ArmorEditor)
        self.arcane_defense.setMaximum(9999)
        self.arcane_defense.setObjectName(_fromUtf8("arcane_defense"))
        self.horizontalLayout.addWidget(self.arcane_defense)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cost = QtGui.QSpinBox(ArmorEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName(_fromUtf8("cost"))
        self.horizontalLayout_2.addWidget(self.cost)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(ArmorEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_6 = QtGui.QLabel(ArmorEditor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.physical_defense = QtGui.QSpinBox(ArmorEditor)
        self.physical_defense.setObjectName(_fromUtf8("physical_defense"))
        self.horizontalLayout_3.addWidget(self.physical_defense)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 6, 2, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.reflex = QtGui.QSpinBox(ArmorEditor)
        self.reflex.setObjectName(_fromUtf8("reflex"))
        self.horizontalLayout_5.addWidget(self.reflex)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_5, 7, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem5 = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(ArmorEditor)
        QtCore.QMetaObject.connectSlotsByName(ArmorEditor)
        ArmorEditor.setTabOrder(self.name, self.cost)
        ArmorEditor.setTabOrder(self.cost, self.type)
        ArmorEditor.setTabOrder(self.type, self.arcane_defense)

    def retranslateUi(self, ArmorEditor):
        ArmorEditor.setWindowTitle(QtGui.QApplication.translate("ArmorEditor", "ArmorEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ArmorEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ArmorEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ArmorEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ArmorEditor", "Arcane Defense: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ArmorEditor", "Physical Defense: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ArmorEditor", "Reflex", None, QtGui.QApplication.UnicodeUTF8))

