# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MonsterEditor.ui'
#
# Created: Sun Aug 21 12:56:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MonsterEditor(object):
    def setupUi(self, MonsterEditor):
        MonsterEditor.setObjectName(_fromUtf8("MonsterEditor"))
        MonsterEditor.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(MonsterEditor)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(MonsterEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(MonsterEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(MonsterEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.root_object = QtGui.QComboBox(MonsterEditor)
        self.root_object.setEditable(True)
        self.root_object.setObjectName(_fromUtf8("root_object"))
        self.gridLayout.addWidget(self.root_object, 1, 1, 1, 1)
        self.action_set = QtGui.QComboBox(MonsterEditor)
        self.action_set.setObjectName(_fromUtf8("action_set"))
        self.gridLayout.addWidget(self.action_set, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(MonsterEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.gridLayout)
        self.monster_image = QtGui.QLabel(MonsterEditor)
        self.monster_image.setMinimumSize(QtCore.QSize(150, 150))
        self.monster_image.setMaximumSize(QtCore.QSize(150, 150))
        self.monster_image.setFrameShape(QtGui.QFrame.Box)
        self.monster_image.setLineWidth(2)
        self.monster_image.setText(_fromUtf8(""))
        self.monster_image.setScaledContents(True)
        self.monster_image.setObjectName(_fromUtf8("monster_image"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.monster_image)

        self.retranslateUi(MonsterEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), MonsterEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(MonsterEditor)

    def retranslateUi(self, MonsterEditor):
        MonsterEditor.setWindowTitle(QtGui.QApplication.translate("MonsterEditor", "MonsterEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MonsterEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MonsterEditor", "Root Object: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MonsterEditor", "Action Set: ", None, QtGui.QApplication.UnicodeUTF8))

