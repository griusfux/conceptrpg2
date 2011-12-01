# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StatusEditor.ui'
#
# Created: Sat Nov 26 14:06:04 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StatusEditor(object):
    def setupUi(self, StatusEditor):
        StatusEditor.setObjectName(_fromUtf8("StatusEditor"))
        StatusEditor.resize(400, 301)
        self.verticalLayout = QtGui.QVBoxLayout(StatusEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(StatusEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.name = QtGui.QLineEdit(StatusEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.horizontalLayout_5.addWidget(self.name)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.pushButton = QtGui.QPushButton(StatusEditor)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(StatusEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), StatusEditor.modified)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("pressed()")), StatusEditor.edit_text)
        QtCore.QMetaObject.connectSlotsByName(StatusEditor)

    def retranslateUi(self, StatusEditor):
        StatusEditor.setWindowTitle(QtGui.QApplication.translate("StatusEditor", "StatusEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StatusEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("StatusEditor", "Edit Python File", None, QtGui.QApplication.UnicodeUTF8))

