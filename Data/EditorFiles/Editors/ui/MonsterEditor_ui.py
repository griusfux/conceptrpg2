# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MonsterEditor.ui'
#
# Created: Sat Sep 25 15:10:27 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MonsterEditor(object):
    def setupUi(self, MonsterEditor):
        MonsterEditor.setObjectName("MonsterEditor")
        MonsterEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MonsterEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(MonsterEditor)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(MonsterEditor)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(MonsterEditor)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ai_start_state = QtGui.QLineEdit(MonsterEditor)
        self.ai_start_state.setObjectName("ai_start_state")
        self.gridLayout.addWidget(self.ai_start_state, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(MonsterEditor)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.ai_keywords = QtGui.QListWidget(MonsterEditor)
        self.ai_keywords.setObjectName("ai_keywords")
        self.gridLayout.addWidget(self.ai_keywords, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(MonsterEditor)
        QtCore.QMetaObject.connectSlotsByName(MonsterEditor)

    def retranslateUi(self, MonsterEditor):
        MonsterEditor.setWindowTitle(QtGui.QApplication.translate("MonsterEditor", "MonsterEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MonsterEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MonsterEditor", "Ai Start State: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MonsterEditor", "Ai Keywords: ", None, QtGui.QApplication.UnicodeUTF8))

