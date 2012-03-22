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

from PySide.QtGui import *
from .BaseEditor import BaseEditor
from .ui.MonsterEditor_ui import Ui_MonsterEditor
from ..common import get_blender_objects

from Scripts.packages import ActionSet

import json

class MonsterEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_MonsterEditor)
		ui = self.ui
				
		# Fill combo boxes
		ui.root_object.addItems(get_blender_objects(data))
		ui.action_set.addItems([i.name for i in ActionSet.get_package_list()])

		with open(data._schema) as f:
			schema = json.loads(f.read())
			element = eval(schema['element'])

		ui.element.addItems([i.title() for i in element])
		
		# Setup the values
		ui.name.setText(data.name)
		idx = ui.root_object.findText(data.root_object)
		if idx < 0:
			ui.root_object.setEditText(data.root_object)
		else:
			ui.root_object.setCurrentIndex(ui.root_object.findText(data.root_object))
		ui.action_set.setCurrentIndex(ui.action_set.findText(data.action_set))
		ui.element.setCurrentIndex(ui.element.findText(data.element.title()))
		ui.hp_per_level.setValue(data.hp_per_level)
		ui.level_adjustment.setValue(data.level_adjustment)
		ui.xp_reward.setValue(data.xp_reward)
		ui.size.setValue(data.size)
		ui.speed.setValue(data.speed)
		
		# Affinities
		ui.fire.setValue(data.affinities['FIRE'])
		ui.storm.setValue(data.affinities['STORM'])
		ui.death.setValue(data.affinities['DEATH'])
		ui.water.setValue(data.affinities['WATER'])
		ui.earth.setValue(data.affinities['EARTH'])
		ui.holy.setValue(data.affinities['HOLY'])
		
		
	def save(self):
		data = self.data
		ui = self.ui
				
		data.name = ui.name.text()
		data.root_object = ui.root_object.currentText()
		data.action_set = ui.action_set.currentText()
		data.element = ui.element.currentText().upper()
		data.hp_per_level = ui.hp_per_level.value()
		data.level_adjustment = ui.level_adjustment.value()
		data.xp_reward = ui.xp_reward.value()
		data.size = ui.size.value()
		data.speed = ui.speed.value()
		
		# Affinities
		data.affinities['FIRE'] = ui.fire.value()
		data.affinities['STORM'] = ui.storm.value()
		data.affinities['DEATH'] = ui.death.value()
		data.affinities['WATER'] = ui.water.value()
		data.affinities['EARTH'] = ui.earth.value()
		data.affinities['HOLY'] = ui.holy.value()