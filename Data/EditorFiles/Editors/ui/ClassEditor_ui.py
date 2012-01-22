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

# Form implementation generated from reading ui file 'ClassEditor.ui'
#
# Created: Tue Sep 27 20:18:27 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ClassEditor(object):
    def setupUi(self, ClassEditor):
        ClassEditor.setObjectName(_fromUtf8("ClassEditor"))
        ClassEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ClassEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ClassEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(ClassEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(ClassEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.starting_armor = QtGui.QComboBox(ClassEditor)
        self.starting_armor.setObjectName(_fromUtf8("starting_armor"))
        self.gridLayout.addWidget(self.starting_armor, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(ClassEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.starting_weapon = QtGui.QComboBox(ClassEditor)
        self.starting_weapon.setObjectName(_fromUtf8("starting_weapon"))
        self.gridLayout.addWidget(self.starting_weapon, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ClassEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), ClassEditor.modified)
        QtCore.QObject.connect(self.starting_armor, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), ClassEditor.modified)
        QtCore.QObject.connect(self.starting_weapon, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), ClassEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(ClassEditor)

    def retranslateUi(self, ClassEditor):
        ClassEditor.setWindowTitle(QtGui.QApplication.translate("ClassEditor", "ClassEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ClassEditor", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ClassEditor", "Starting Armor: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ClassEditor", "Starting Weapon: ", None, QtGui.QApplication.UnicodeUTF8))

