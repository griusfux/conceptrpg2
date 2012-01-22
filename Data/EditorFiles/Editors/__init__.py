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

from .ArmorEditor import ArmorEditor
from .ClassEditor import ClassEditor
from .ItemEditor import ItemEditor
from .MapEditor import MapEditor
from .MonsterEditor import MonsterEditor
from .PowerEditor import PowerEditor
from .RaceEditor import RaceEditor
from .StatusEditor import StatusEditor
from .WeaponEditor import WeaponEditor

# import EditorFiles.Editors.ArmorEditor as ArmorEditor
# import EditorFiles.Editors.ClassEditor as ClassEditor
# import EditorFiles.Editors.ItemEditor as ItemEditor
# import EditorFiles.Editors.MapEditor as MapEditor
# import EditorFiles.Editors.MonsterEditor as MonsterEditor

# import imp

# EDITORS = {}

# def reload_editors():
	# global EDITORS
	
	# reload(ArmorEditor)
	# reload(ClassEditor)
	# reload(ItemEditor)
	# reload(MonsterEditor)
	
	# EDITORS = {
		# 'Armors': ArmorEditor.ArmorEditor,
		# 'Items': ItemEditor.ItemEditor,
		# 'Maps': MapEditor.MapEditor,
		# }
		
# reload_editors()