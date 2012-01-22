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

# Form implementation generated from reading ui file 'RaceEditor.ui'
#
# Created: Sun Aug 21 13:04:05 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RaceEditor(object):
    def setupUi(self, RaceEditor):
        RaceEditor.setObjectName(_fromUtf8("RaceEditor"))
        RaceEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(RaceEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.name = QtGui.QLineEdit(RaceEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(RaceEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.root_object = QtGui.QComboBox(RaceEditor)
        self.root_object.setEditable(True)
        self.root_object.setObjectName(_fromUtf8("root_object"))
        self.gridLayout.addWidget(self.root_object, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(RaceEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.action_set = QtGui.QComboBox(RaceEditor)
        self.action_set.setObjectName(_fromUtf8("action_set"))
        self.gridLayout.addWidget(self.action_set, 3, 2, 1, 1)
        self.label = QtGui.QLabel(RaceEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.gridLayout)
        self.data_image = QtGui.QLabel(RaceEditor)
        self.data_image.setMinimumSize(QtCore.QSize(150, 150))
        self.data_image.setMaximumSize(QtCore.QSize(150, 150))
        self.data_image.setFrameShape(QtGui.QFrame.Box)
        self.data_image.setLineWidth(2)
        self.data_image.setText(_fromUtf8(""))
        self.data_image.setScaledContents(True)
        self.data_image.setObjectName(_fromUtf8("data_image"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.data_image)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(RaceEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), RaceEditor.modified)
        QtCore.QObject.connect(self.root_object, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), RaceEditor.modified)
        QtCore.QObject.connect(self.action_set, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), RaceEditor.modified)
        QtCore.QObject.connect(self.root_object, QtCore.SIGNAL(_fromUtf8("editTextChanged(QString)")), RaceEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(RaceEditor)

    def retranslateUi(self, RaceEditor):
        RaceEditor.setWindowTitle(QtGui.QApplication.translate("RaceEditor", "RaceEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RaceEditor", "Root Object: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RaceEditor", "Action Set: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RaceEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))

