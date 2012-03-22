# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WeaponEditor.ui'
#
# Created: Sat Sep  3 15:57:49 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WeaponEditor(object):
    def setupUi(self, WeaponEditor):
        WeaponEditor.setObjectName(_fromUtf8("WeaponEditor"))
        WeaponEditor.resize(400, 322)
        self.verticalLayout = QtGui.QVBoxLayout(WeaponEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.data_image = QtGui.QLabel(WeaponEditor)
        self.data_image.setMinimumSize(QtCore.QSize(150, 150))
        self.data_image.setMaximumSize(QtCore.QSize(150, 150))
        self.data_image.setFrameShape(QtGui.QFrame.Box)
        self.data_image.setLineWidth(2)
        self.data_image.setText(_fromUtf8(""))
        self.data_image.setScaledContents(True)
        self.data_image.setObjectName(_fromUtf8("data_image"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.data_image)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(WeaponEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(WeaponEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(WeaponEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cost = QtGui.QSpinBox(WeaponEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName(_fromUtf8("cost"))
        self.horizontalLayout_2.addWidget(self.cost)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(WeaponEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.description = QtGui.QPlainTextEdit(WeaponEditor)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout.addWidget(self.description, 2, 2, 1, 1)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.gridLayout)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(20, 85, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(WeaponEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(WeaponEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(WeaponEditor)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.weight = QtGui.QSpinBox(WeaponEditor)
        self.weight.setMinimum(-5)
        self.weight.setMaximum(5)
        self.weight.setObjectName(_fromUtf8("weight"))
        self.horizontalLayout.addWidget(self.weight)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.type = QtGui.QComboBox(WeaponEditor)
        self.type.setEditable(False)
        self.type.setObjectName(_fromUtf8("type"))
        self.gridLayout_2.addWidget(self.type, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.range = QtGui.QSpinBox(WeaponEditor)
        self.range.setMinimum(-5)
        self.range.setMaximum(5)
        self.range.setObjectName(_fromUtf8("range"))
        self.horizontalLayout_3.addWidget(self.range)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(WeaponEditor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.accuracy = QtGui.QSpinBox(WeaponEditor)
        self.accuracy.setMinimum(-5)
        self.accuracy.setMaximum(5)
        self.accuracy.setObjectName(_fromUtf8("accuracy"))
        self.horizontalLayout_4.addWidget(self.accuracy)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(WeaponEditor)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.hands = QtGui.QComboBox(WeaponEditor)
        self.hands.setObjectName(_fromUtf8("hands"))
        self.horizontalLayout_5.addWidget(self.hands)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(WeaponEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.cost, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.type, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.weight, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.range, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.accuracy, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.hands, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), WeaponEditor.modified)
        QtCore.QObject.connect(self.description, QtCore.SIGNAL(_fromUtf8("textChanged()")), WeaponEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(WeaponEditor)
        WeaponEditor.setTabOrder(self.name, self.cost)
        WeaponEditor.setTabOrder(self.cost, self.type)
        WeaponEditor.setTabOrder(self.type, self.weight)
        WeaponEditor.setTabOrder(self.weight, self.range)
        WeaponEditor.setTabOrder(self.range, self.accuracy)
        WeaponEditor.setTabOrder(self.accuracy, self.hands)

    def retranslateUi(self, WeaponEditor):
        WeaponEditor.setWindowTitle(QtGui.QApplication.translate("WeaponEditor", "WeaponEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WeaponEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("WeaponEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("WeaponEditor", "Description: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("WeaponEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("WeaponEditor", "Weight: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("WeaponEditor", "Range: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("WeaponEditor", "Accuracy: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("WeaponEditor", "Hands: ", None, QtGui.QApplication.UnicodeUTF8))

