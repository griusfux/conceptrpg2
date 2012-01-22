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

# Form implementation generated from reading ui file 'MapEditor.ui'
#
# Created: Sun Aug 21 00:54:42 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapEditor(object):
    def setupUi(self, MapEditor):
        MapEditor.setObjectName(_fromUtf8("MapEditor"))
        MapEditor.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MapEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(MapEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(MapEditor)
        self.name.setEnabled(True)
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.encounter_deck = QtGui.QLineEdit(MapEditor)
        self.encounter_deck.setEnabled(True)
        self.encounter_deck.setObjectName(_fromUtf8("encounter_deck"))
        self.gridLayout.addWidget(self.encounter_deck, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(MapEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(MapEditor)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add_tile = QtGui.QPushButton(MapEditor)
        self.add_tile.setObjectName(_fromUtf8("add_tile"))
        self.horizontalLayout.addWidget(self.add_tile)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tile_tabs = QtGui.QTabWidget(MapEditor)
        self.tile_tabs.setObjectName(_fromUtf8("tile_tabs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.start_view = QtGui.QTreeView(self.tab)
        self.start_view.setObjectName(_fromUtf8("start_view"))
        self.verticalLayout_2.addWidget(self.start_view)
        self.tile_tabs.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.room_view = QtGui.QTreeView(self.tab_2)
        self.room_view.setObjectName(_fromUtf8("room_view"))
        self.verticalLayout_3.addWidget(self.room_view)
        self.tile_tabs.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.corridor_view = QtGui.QTreeView(self.tab_3)
        self.corridor_view.setObjectName(_fromUtf8("corridor_view"))
        self.verticalLayout_4.addWidget(self.corridor_view)
        self.tile_tabs.addTab(self.tab_3, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.end_view = QtGui.QTreeView(self.tab_5)
        self.end_view.setObjectName(_fromUtf8("end_view"))
        self.verticalLayout_6.addWidget(self.end_view)
        self.tile_tabs.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_6)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.stair_view = QtGui.QTreeView(self.tab_6)
        self.stair_view.setObjectName(_fromUtf8("stair_view"))
        self.verticalLayout_7.addWidget(self.stair_view)
        self.tile_tabs.addTab(self.tab_6, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tile_tabs)

        self.retranslateUi(MapEditor)
        self.tile_tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.name, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), MapEditor.modified)
        QtCore.QObject.connect(self.encounter_deck, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), MapEditor.modified)
        QtCore.QObject.connect(self.add_tile, QtCore.SIGNAL(_fromUtf8("clicked()")), MapEditor.modified)
        QtCore.QMetaObject.connectSlotsByName(MapEditor)

    def retranslateUi(self, MapEditor):
        MapEditor.setWindowTitle(QtGui.QApplication.translate("MapEditor", "MapEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MapEditor", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MapEditor", "Encounter Deck: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MapEditor", "Tiles", None, QtGui.QApplication.UnicodeUTF8))
        self.add_tile.setText(QtGui.QApplication.translate("MapEditor", "Add &Tile", None, QtGui.QApplication.UnicodeUTF8))
        self.tile_tabs.setTabText(self.tile_tabs.indexOf(self.tab), QtGui.QApplication.translate("MapEditor", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.tile_tabs.setTabText(self.tile_tabs.indexOf(self.tab_2), QtGui.QApplication.translate("MapEditor", "Room", None, QtGui.QApplication.UnicodeUTF8))
        self.tile_tabs.setTabText(self.tile_tabs.indexOf(self.tab_3), QtGui.QApplication.translate("MapEditor", "Corridor", None, QtGui.QApplication.UnicodeUTF8))
        self.tile_tabs.setTabText(self.tile_tabs.indexOf(self.tab_5), QtGui.QApplication.translate("MapEditor", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.tile_tabs.setTabText(self.tile_tabs.indexOf(self.tab_6), QtGui.QApplication.translate("MapEditor", "Stair", None, QtGui.QApplication.UnicodeUTF8))

