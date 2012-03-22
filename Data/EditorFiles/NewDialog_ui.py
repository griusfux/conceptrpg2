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

# Form implementation generated from reading ui file 'NewDialog.ui'
#
# Created: Sat Sep 25 21:32:55 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewDialog(object):
    def setupUi(self, NewDialog):
        NewDialog.setObjectName("NewDialog")
        NewDialog.resize(280, 121)
        NewDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(NewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(NewDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(NewDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.package_name = QtGui.QLineEdit(NewDialog)
        self.package_name.setObjectName("package_name")
        self.gridLayout.addWidget(self.package_name, 0, 1, 1, 1)
        self.package_type = QtGui.QComboBox(NewDialog)
        self.package_type.setObjectName("package_type")
        self.gridLayout.addWidget(self.package_type, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(NewDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewDialog)
        NewDialog.setTabOrder(self.package_name, self.package_type)
        NewDialog.setTabOrder(self.package_type, self.buttonBox)

    def retranslateUi(self, NewDialog):
        NewDialog.setWindowTitle(QtGui.QApplication.translate("NewDialog", "New Package", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewDialog", "Package Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewDialog", "Package Type: ", None, QtGui.QApplication.UnicodeUTF8))

