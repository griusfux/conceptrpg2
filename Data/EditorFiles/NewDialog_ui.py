# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewDialog.ui'
#
# Created: Sat Sep 25 21:32:55 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

