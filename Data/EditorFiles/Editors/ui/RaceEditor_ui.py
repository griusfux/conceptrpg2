# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RaceEditor.ui'
#
# Created: Sat Aug 20 22:49:01 2011
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
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
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.race_image = QtGui.QLabel(RaceEditor)
        self.race_image.setMinimumSize(QtCore.QSize(150, 150))
        self.race_image.setMaximumSize(QtCore.QSize(150, 150))
        self.race_image.setFrameShape(QtGui.QFrame.Box)
        self.race_image.setLineWidth(2)
        self.race_image.setText(_fromUtf8(""))
        self.race_image.setScaledContents(True)
        self.race_image.setObjectName(_fromUtf8("race_image"))
        self.horizontalLayout.addWidget(self.race_image)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(RaceEditor)
        QtCore.QMetaObject.connectSlotsByName(RaceEditor)

    def retranslateUi(self, RaceEditor):
        RaceEditor.setWindowTitle(QtGui.QApplication.translate("RaceEditor", "RaceEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RaceEditor", "Root Object: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RaceEditor", "Action Set: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RaceEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))

