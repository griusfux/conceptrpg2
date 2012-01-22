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

# Form implementation generated from reading ui file 'ItemEditor.ui'
#
# Created: Sun Aug 21 13:02:52 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ItemEditor(object):
    def setupUi(self, ItemEditor):
        ItemEditor.setObjectName(_fromUtf8("ItemEditor"))
        ItemEditor.resize(400, 300)
        self.formLayout_2 = QtGui.QFormLayout(ItemEditor)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.data_image = QtGui.QLabel(ItemEditor)
        self.data_image.setMinimumSize(QtCore.QSize(150, 150))
        self.data_image.setMaximumSize(QtCore.QSize(150, 150))
        self.data_image.setFrameShape(QtGui.QFrame.Box)
        self.data_image.setLineWidth(2)
        self.data_image.setText(_fromUtf8(""))
        self.data_image.setScaledContents(True)
        self.data_image.setObjectName(_fromUtf8("data_image"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.data_image)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ItemEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.name = QtGui.QLineEdit(ItemEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 4, 1, 1)
        self.label_2 = QtGui.QLabel(ItemEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cost = QtGui.QSpinBox(ItemEditor)
        self.cost.setMaximum(9999)
        self.cost.setObjectName(_fromUtf8("cost"))
        self.horizontalLayout.addWidget(self.cost)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.gridLayout)

        self.retranslateUi(ItemEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), ItemEditor.modified)
        QtCore.QObject.connect(self.cost, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), ItemEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(ItemEditor)
        ItemEditor.setTabOrder(self.name, self.cost)

    def retranslateUi(self, ItemEditor):
        ItemEditor.setWindowTitle(QtGui.QApplication.translate("ItemEditor", "ItemEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ItemEditor", "Name:           ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ItemEditor", "Cost:", None, QtGui.QApplication.UnicodeUTF8))

