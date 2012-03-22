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

# Form implementation generated from reading ui file 'SettingsDialog.ui'
#
# Created: Sun Nov 27 00:56:36 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(400, 300)
        self.gridLayout_2 = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.blender_path = QtGui.QLineEdit(SettingsDialog)
        self.blender_path.setObjectName(_fromUtf8("blender_path"))
        self.horizontalLayout.addWidget(self.blender_path)
        self.browse_button = QtGui.QPushButton(SettingsDialog)
        self.browse_button.setObjectName(_fromUtf8("browse_button"))
        self.horizontalLayout.addWidget(self.browse_button)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(SettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.text_editor_path = QtGui.QLineEdit(SettingsDialog)
        self.text_editor_path.setObjectName(_fromUtf8("text_editor_path"))
        self.horizontalLayout_2.addWidget(self.text_editor_path)
        self.tebrowsebutton = QtGui.QPushButton(SettingsDialog)
        self.tebrowsebutton.setObjectName(_fromUtf8("tebrowsebutton"))
        self.horizontalLayout_2.addWidget(self.tebrowsebutton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialog.reject)
        QtCore.QObject.connect(self.browse_button, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.find_blender)
        QtCore.QObject.connect(self.tebrowsebutton, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.find_text_editor)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsDialog", "Blender Path: ", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_button.setText(QtGui.QApplication.translate("SettingsDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SettingsDialog", "Text Editor:", None, QtGui.QApplication.UnicodeUTF8))
        self.tebrowsebutton.setText(QtGui.QApplication.translate("SettingsDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))

