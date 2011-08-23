# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MonsterEditor.ui'
#
# Created: Mon Aug 22 22:49:58 2011
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
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
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
        self.label_2 = QtGui.QLabel(MonsterEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.element = QtGui.QComboBox(MonsterEditor)
        self.element.setObjectName(_fromUtf8("element"))
        self.gridLayout.addWidget(self.element, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(MonsterEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.hp_per_level = QtGui.QSpinBox(MonsterEditor)
        self.hp_per_level.setObjectName(_fromUtf8("hp_per_level"))
        self.horizontalLayout.addWidget(self.hp_per_level)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(MonsterEditor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.level_adjustment = QtGui.QSpinBox(MonsterEditor)
        self.level_adjustment.setMinimum(-10)
        self.level_adjustment.setMaximum(10)
        self.level_adjustment.setObjectName(_fromUtf8("level_adjustment"))
        self.horizontalLayout_2.addWidget(self.level_adjustment)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.gridLayout)
        self.data_image = QtGui.QLabel(MonsterEditor)
        self.data_image.setMinimumSize(QtCore.QSize(150, 150))
        self.data_image.setMaximumSize(QtCore.QSize(150, 150))
        self.data_image.setFrameShape(QtGui.QFrame.Box)
        self.data_image.setLineWidth(2)
        self.data_image.setText(_fromUtf8(""))
        self.data_image.setScaledContents(True)
        self.data_image.setObjectName(_fromUtf8("data_image"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.data_image)

        self.retranslateUi(MonsterEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.root_object, QtCore.SIGNAL(_fromUtf8("editTextChanged(QString)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.action_set, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.element, QtCore.SIGNAL(_fromUtf8("editTextChanged(QString)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.hp_per_level, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.level_adjustment, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), MonsterEditor.modified)
        QtCore.QObject.connect(self.element, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MonsterEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(MonsterEditor)

    def retranslateUi(self, MonsterEditor):
        MonsterEditor.setWindowTitle(QtGui.QApplication.translate("MonsterEditor", "MonsterEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MonsterEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MonsterEditor", "Root Object: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MonsterEditor", "Action Set: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MonsterEditor", "Element: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MonsterEditor", "HP Per Level: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MonsterEditor", "Level Adjustment: ", None, QtGui.QApplication.UnicodeUTF8))

