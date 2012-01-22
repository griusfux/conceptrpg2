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

import random

#===============================================================================
# Modifer base classes
#===============================================================================

class ItemModifier:
    mod_type = ''
    
    def __init__(self, base, level):
        self._base = base
        self.level = level
        
    @property
    def _modifiers(self):
        return self._base._modifiers

class ArmorModifier(ItemModifier):
    mod_type = 'Armor'
    
    def __init__(self, armor, level):
        ItemModifier.__init__(self, armor, level)
        self.type = armor.type
    
    @property
    def _arcane_defense(self):
        return self._base._arcane_defense
    
    @property
    def _physical_defense(self):
        return self._base._physical_defense
    
    @property
    def _reflex(self):
        return self._base._reflex
    
class WeaponModifier(ItemModifier):
    mod_type = 'Weapon'
    
    def __init__(self, weapon, level):
        ItemModifier.__init__(self, weapon, level)
        self.type = weapon.type
        
    @property
    def _range(self):
        return self._base._range
    
    @property
    def _accuracy(self):
        return self._base._accuracy
    
    @property
    def _cost(self):
        return self._base._cost
    
#===============================================================================
# Armor Modifiers
#===============================================================================
class arcane_defense(ArmorModifier):
    @property
    def _arcane_defense(self):
        return self._base._arcane_defense + self.level
    
#===============================================================================
# Weapon Modifiers
#===============================================================================
class accuracy(WeaponModifier):
    
    mod_names = [
                 "Troll Eye",
                 "Bug Eye",
                 "Cat Eye",
                 "Hawk Eye I",
                 "Hawk Eye II",
                 "Hawk Eye III"
                 ]
    
    def __init__(self, base, level):
        WeaponModifier.__init__(self, base, level)
        
        self._acc = random.randint(1, level)
        self.name = self.mod_names[level]
    
    @property
    def _accuracy(self):
        return self._base._accuracy + self._acc
    
    @property
    def _modifiers(self):
        return self._base._modifiers + ["+%d accuracy (%s)" % (self._acc, self.name)]
        