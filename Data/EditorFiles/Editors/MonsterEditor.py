from PyQt4.QtGui import *

class MonsterEditor(QFrame):
	def __init__(self, parent, img, data):
		QFrame.__init__(self, parent)
		self.setFrameShape(QFrame.StyledPanel)
		
		self.data = data
		
		# A font object to use
		font = QFont()
		
		# Name
		label = QLabel(data.name + "\tLv. " + str(data.level), self)
		font.setPointSize(18)
		label.setFont(font)
		
		# Picture		
		pic = QLabel(self)
		pic.setPixmap(QPixmap.fromImage(img.scaled(100, 100)))
		pic.setMargin(20)
		
		# Stats
		stats = QVBoxLayout()
		str_lbl = QLabel("Str: "+str(data.str_ab), self)
		dex_lbl = QLabel("Dex: "+str(data.dex_ab), self)
		con_lbl = QLabel("Con: "+str(data.con_ab), self)
		int_lbl = QLabel("Int: "+str(data.int_ab), self)
		wis_lbl = QLabel("Wis: "+str(data.wis_ab), self)
		cha_lbl = QLabel("Cha: "+str(data.cha_ab), self)
		stats.addWidget(str_lbl)
		stats.addWidget(dex_lbl)
		stats.addWidget(con_lbl)
		stats.addWidget(int_lbl)
		stats.addWidget(wis_lbl)
		stats.addWidget(cha_lbl)
		stats.addStretch(1)
		
		hbox = QHBoxLayout()
		hbox.addWidget(pic, 1)
		hbox.addLayout(stats, 1)
		
		vbox = QVBoxLayout(self)
		vbox.addWidget(label)
		vbox.addLayout(hbox)
		vbox.addStretch(1)
		
		
		self.setLayout(vbox)