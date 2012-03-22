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

# Form implementation generated from reading ui file 'PowerEditor.ui'
#
# Created: Mon Aug 22 16:52:07 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PowerEditor(object):
    def setupUi(self, PowerEditor):
        PowerEditor.setObjectName(_fromUtf8("PowerEditor"))
        PowerEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PowerEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(PowerEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.name = QtGui.QLineEdit(PowerEditor)
        self.name.setObjectName(_fromUtf8("name"))
        self.horizontalLayout_5.addWidget(self.name)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(PowerEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtGui.QLabel(PowerEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.delivery = QtGui.QComboBox(PowerEditor)
        self.delivery.setObjectName(_fromUtf8("delivery"))
        self.horizontalLayout_3.addWidget(self.delivery)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 6, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.shape_modifier = QtGui.QSpinBox(PowerEditor)
        self.shape_modifier.setMaximum(360)
        self.shape_modifier.setObjectName(_fromUtf8("shape_modifier"))
        self.horizontalLayout_4.addWidget(self.shape_modifier)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 6, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cool_down = QtGui.QSpinBox(PowerEditor)
        self.cool_down.setMinimum(1)
        self.cool_down.setObjectName(_fromUtf8("cool_down"))
        self.horizontalLayout.addWidget(self.cool_down)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 6, 1, 1)
        self.element = QtGui.QComboBox(PowerEditor)
        self.element.setObjectName(_fromUtf8("element"))
        self.gridLayout.addWidget(self.element, 2, 1, 1, 1)
        self.effect_shape = QtGui.QComboBox(PowerEditor)
        self.effect_shape.setObjectName(_fromUtf8("effect_shape"))
        self.gridLayout.addWidget(self.effect_shape, 3, 1, 1, 1)
        self.tier = QtGui.QSpinBox(PowerEditor)
        self.tier.setMinimum(1)
        self.tier.setMaximum(5)
        self.tier.setObjectName(_fromUtf8("tier"))
        self.gridLayout.addWidget(self.tier, 5, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PowerEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 3, 1, 1)
        self.label_5 = QtGui.QLabel(PowerEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.label_8 = QtGui.QLabel(PowerEditor)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 5, 3, 1, 1)
        self.label_7 = QtGui.QLabel(PowerEditor)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_9 = QtGui.QLabel(PowerEditor)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 3, 1, 1)
        self.distance = QtGui.QSpinBox(PowerEditor)
        self.distance.setObjectName(_fromUtf8("distance"))
        self.gridLayout.addWidget(self.distance, 4, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_10 = QtGui.QLabel(PowerEditor)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout.addWidget(self.label_10)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.tm_enemies = QtGui.QCheckBox(PowerEditor)
        self.tm_enemies.setObjectName(_fromUtf8("tm_enemies"))
        self.horizontalLayout_6.addWidget(self.tm_enemies)
        self.tm_self = QtGui.QCheckBox(PowerEditor)
        self.tm_self.setObjectName(_fromUtf8("tm_self"))
        self.horizontalLayout_6.addWidget(self.tm_self)
        self.tm_allies = QtGui.QCheckBox(PowerEditor)
        self.tm_allies.setObjectName(_fromUtf8("tm_allies"))
        self.horizontalLayout_6.addWidget(self.tm_allies)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.label_6 = QtGui.QLabel(PowerEditor)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.description = QtGui.QPlainTextEdit(PowerEditor)
        self.description.setObjectName(_fromUtf8("description"))
        self.verticalLayout.addWidget(self.description)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(PowerEditor)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), PowerEditor.modified)
        QtCore.QObject.connect(self.element, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.delivery, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.effect_shape, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.shape_modifier, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.distance, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.distance, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.cool_down, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.tier, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.description, QtCore.SIGNAL(_fromUtf8("textChanged()")), PowerEditor.modified)
        QtCore.QObject.connect(self.tm_enemies, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.tm_self, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), PowerEditor.modified)
        QtCore.QObject.connect(self.tm_allies, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), PowerEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(PowerEditor)
        PowerEditor.setTabOrder(self.name, self.element)
        PowerEditor.setTabOrder(self.element, self.delivery)
        PowerEditor.setTabOrder(self.delivery, self.effect_shape)
        PowerEditor.setTabOrder(self.effect_shape, self.shape_modifier)
        PowerEditor.setTabOrder(self.shape_modifier, self.distance)
        PowerEditor.setTabOrder(self.distance, self.tier)
        PowerEditor.setTabOrder(self.tier, self.cool_down)
        PowerEditor.setTabOrder(self.cool_down, self.description)

    def retranslateUi(self, PowerEditor):
        PowerEditor.setWindowTitle(QtGui.QApplication.translate("PowerEditor", "PowerEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PowerEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PowerEditor", "Effect Shape: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PowerEditor", "Element:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PowerEditor", "Shape Modifier: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PowerEditor", "Delivery:    ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PowerEditor", "Cool Down: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PowerEditor", "Tier:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("PowerEditor", "Distance:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("PowerEditor", "Target Mask:", None, QtGui.QApplication.UnicodeUTF8))
        self.tm_enemies.setText(QtGui.QApplication.translate("PowerEditor", "Enemies", None, QtGui.QApplication.UnicodeUTF8))
        self.tm_self.setText(QtGui.QApplication.translate("PowerEditor", "Self", None, QtGui.QApplication.UnicodeUTF8))
        self.tm_allies.setText(QtGui.QApplication.translate("PowerEditor", "Allies", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PowerEditor", "Description:", None, QtGui.QApplication.UnicodeUTF8))

