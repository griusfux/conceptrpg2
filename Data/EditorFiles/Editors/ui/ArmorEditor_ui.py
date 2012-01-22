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

# Form implementation generated from reading ui file 'ArmorEditor.ui'
#
# Created: Sat Sep  3 15:57:51 2011
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
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cost = QtGui.QSpinBox(ArmorEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName(_fromUtf8("cost"))
        self.horizontalLayout_2.addWidget(self.cost)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.name = QtGui.QLineEdit(ArmorEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout_2.addWidget(self.name, 1, 1, 1, 1)
        self.label = QtGui.QLabel(ArmorEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ArmorEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_7 = QtGui.QLabel(ArmorEditor)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.description = QtGui.QPlainTextEdit(ArmorEditor)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout_2.addWidget(self.description, 3, 1, 1, 1)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.gridLayout_2)
        self.data_image = QtGui.QLabel(ArmorEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_image.sizePolicy().hasHeightForWidth())
        self.data_image.setSizePolicy(sizePolicy)
        self.data_image.setMinimumSize(QtCore.QSize(150, 150))
        self.data_image.setMaximumSize(QtCore.QSize(150, 150))
        self.data_image.setFrameShape(QtGui.QFrame.Box)
        self.data_image.setLineWidth(2)
        self.data_image.setText(_fromUtf8(""))
        self.data_image.setScaledContents(True)
        self.data_image.setObjectName(_fromUtf8("data_image"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.data_image)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(ArmorEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(ArmorEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.type = QtGui.QComboBox(ArmorEditor)
        self.type.setEditable(False)
        self.type.setObjectName(_fromUtf8("type"))
        self.gridLayout.addWidget(self.type, 3, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.arcane_defense = QtGui.QSpinBox(ArmorEditor)
        self.arcane_defense.setMaximum(9999)
        self.arcane_defense.setObjectName(_fromUtf8("arcane_defense"))
        self.horizontalLayout.addWidget(self.arcane_defense)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.label_3 = QtGui.QLabel(ArmorEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_6 = QtGui.QLabel(ArmorEditor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.physical_defense = QtGui.QSpinBox(ArmorEditor)
        self.physical_defense.setObjectName(_fromUtf8("physical_defense"))
        self.horizontalLayout_3.addWidget(self.physical_defense)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 2, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.reflex = QtGui.QSpinBox(ArmorEditor)
        self.reflex.setObjectName(_fromUtf8("reflex"))
        self.horizontalLayout_5.addWidget(self.reflex)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(ArmorEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.cost, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.type, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.arcane_defense, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.physical_defense, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.reflex, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ArmorEditor.modified)
        QtCore.QObject.connect(self.description, QtCore.SIGNAL(_fromUtf8("textChanged()")), ArmorEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(ArmorEditor)
        ArmorEditor.setTabOrder(self.cost, self.type)
        ArmorEditor.setTabOrder(self.type, self.arcane_defense)

    def retranslateUi(self, ArmorEditor):
        ArmorEditor.setWindowTitle(QtGui.QApplication.translate("ArmorEditor", "ArmorEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ArmorEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ArmorEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ArmorEditor", "Description: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ArmorEditor", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ArmorEditor", "Arcane Defense: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ArmorEditor", "Physical Defense: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ArmorEditor", "Reflex", None, QtGui.QApplication.UnicodeUTF8))

