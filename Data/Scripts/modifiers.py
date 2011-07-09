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
        