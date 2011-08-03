from .Engine.packages import *

class Map(Package):
    """Map package"""
    
    _ext = 'map'
    _blend = 'map.blend'
    _config = 'map.json'
    _schema = 'Schemas/mapfile.json'
    _dir = 'Maps'
    
class EncounterDeck(Package):
    """Encounter deck package"""
    
    def __init__(self, package_name, new_package=False):
        Package.__init__(self, package_name, new_package)
        
        # Build a deck
        self.deck = []
        
        for card in self.cards:
            self.deck.extend([(card['monster'], card['role']) for i in range(card['count'])])
    
    _ext = 'deck'
    _blend = ''
    _config = 'deck.json'
    _schema = 'Schemas/deckfile.json'
    _dir = 'EncounterDecks'
    
class Monster(Package):
    """Monster package"""
    
    _ext = 'monster'
    _blend = 'monster.blend'
    _config = 'monster.json'
    _schema = 'Schemas/monsterfile.json'
    _dir = 'Monsters'
    
class Race(Package):
    """Race package"""
    
    _ext = 'race'
    _blend = 'race.blend'
    _config = 'race.json'
    _schema = 'Schemas/racefile.json'
    _dir = 'Races'
    _img = 'race.png'
    
class Class(Package):
    """Player class package"""
    
    _ext = 'class'
    _config = 'class.json'
    _schema = 'Schemas/classfile.json'
    _dir = 'Classes'
    _img = 'class.png'

class Power(Package):
    """Power package"""
    
    _ext = 'power'
    _blend = ''
    _config = 'power.json'
    _schema = 'Schemas/powerfile.json'
    _dir = 'Powers/Powers'
    _img = 'power.png'
    
    def __init__(self, package_name, new_package=False):
        Package.__init__(self, package_name, new_package)
        
        # Create a script file if this is a new package
        if new_package:
            open(os.path.join(self._dir, package_name, 'power.py'), 'wb').close()
        
        # Write the script to a temp file
        pyfile = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
        pyfile.write(self._package.read("power.py"))
        pyfile.read() # Not sure why this is needed, but the module isn't properly loaded otherwise
        
        # Load the module
        p = imp.load_source("power", pyfile.name)
        
        # We don't need the temp file anymore, so clean up
        pyfile.close()
        os.remove(pyfile.name)
        try:
            os.remove(pyfile.name.replace('.py', '.pyc'))
        except WindowsError:
            # Probably not the best thing as there could be still useful files in this folder...
            shutil.rmtree(os.path.join(tempfile.gettempdir(), '__pycache__'))

        # Grab the method from the module
        self._use = p.power
        self._push = None
        self._pop = None
        
        # Set up a boolean property to determine if the power is used or not
        self.spent = False
        
        if "PASSIVE" in self.flags:
            self._push = p.push
            self._pop = p.pop
        
    def use(self, controller, user):
        self._use(self, controller, user)
        
    def push(self, controller, user):
        if self._push:
            self._push(self, controller, user)
        else:
            pass
            
    def pop(self, controller, user):
        if self._pop:
            self._pop(self, controller, user)
        else:
            pass
    
    def write(self):
        Package.write(self)
        
           
        
    def pack(self, path):
        Package.pack(self, path)
        
        zip = zipfile.ZipFile(path+'.'+self._ext, "a", zipfile.ZIP_DEFLATED)
        
        # Copy py file
        zip.write(os.path.join(self._path, 'power.py'), arcname='power.py')
        
        zip.close()
        
class Feat(Power):
    _dir = 'Powers/Feats'
    _schema = 'Schemas/featfile.json'
    
class Status(Power):
    _dir = 'Powers/Statuses'
    _schema = 'Schemas/statusfile.json'
    
    def __init__(self, package_name, new_package=False):
        Power.__init__(self, package_name, new_package)
        self.amount = 0
    
        
class Item(Package):
    """Item Package"""
    
    _ext = 'item'
    _config = 'item.json'
    _schema = 'Schemas/itemfile.json'
    _new = 'Schemas/itemfile_new.json'
    _dir = 'Items/Others'
    _img = 'item.png'
    
class Weapon(Item):
    """Weapon Package"""
    
    _config = 'weapon.json'
    _blend = 'weapon.blend'
    _parent_schema = Item._schema
    _schema = 'Schemas/weaponfile.json'
    _dir = 'Items/Weapons'
    _img = 'weapon.png'
    
class Armor(Item):
    """Armor Package"""
    
    _config = 'armor.json'
    _parent_schema = Item._schema
    _schema = 'Schemas/armorfile.json'
    _dir = 'Items/Armors'
    _img = 'armor.png'
    
class ActionSet(Package):
    """Action Set Package"""
    
    _ext = 'as'
    _blend = 'actionset.blend'
    _config = 'actionset.json'
    _schema = 'Schemas/actionsetfile.json'
    _new = 'Schemas/actionsetfile_new.json'
    _dir = 'ActionSets'
    
    def __init__(self, package_name, new_package=False):
        Package.__init__(self, package_name, new_package)
        
        self.actions = {}
        
        for action in self.action_set:
            self.actions[action['name']] = action['actions']
    
class Shop(Package):
    """Shop package"""
    
    _ext = 'shop'
    _blend = 'shop.blend'
    _config = 'shop.json'
    _schema = 'Schemas/shopfile.json'
    _new = 'Schemas/shopfile_new.json'
    _dir = 'Shops'
    
    def __init__(self, package_name, new_package=False):
        Package.__init__(self, package_name, new_package)
        
        # Build item lists
        self.items = []
        self.weapons = []
        self.armors = []
        
        for f in os.listdir(os.path.join('Shops', '.config')):
            if f.lower().startswith(package_name.lower()):
                self._parse_conf(os.path.join('Shops', '.config', f))
                    
    def _parse_conf(self, path):
        curr_list = self.items
        curr_package = Item
    
        with open(path) as conf:
            for line in conf.readlines():
                line = line.strip()
                
                if not line:
                    continue
                elif line == "[Items]":
                    curr_list = self.items
                    curr_package = Item
                elif line == "[Weapons]":
                    curr_list = self.weapons
                    curr_package = Weapon
                elif line == "[Armors]":
                    curr_list = self.armors
                    curr_package = Armor
                else:
                    try:
                        curr_list.append(curr_package(line))
                    except Exception as e:
                        print(e)
                        print("Failed to load package:", line)
                        
class Save(Package):
    """Save package"""
    
    _ext = 'save'
    _config = 'save.json'
    _schema = 'Schemas/savefile.json'
    _new = 'Schemas/savefile_new.json'
    _dir = '../Saves'
    _img = 'save.png'
    
    def __init__(self, package_name, new_package=False):
        Package.__init__(self, package_name, new_package)
        
        # Load up the data file
        try:
            self.data = pickle.loads(self._package.read("data"))
        except IOError:
            self.data = {}
        
    def pack(self, path):
        Package.pack(self, path)
        
        zip = zipfile.ZipFile(path+'.'+self._ext, "a", zipfile.ZIP_DEFLATED)
        
        # Copy data file
        zip.write(os.path.join(self._path, 'data'), arcname='data')
        
        zip.close()
        
    def write(self):
        Package.write(self)
    
        with open(os.path.join(self._path, 'data'), 'wb') as f:
            pickle.dump(self.data, f)
            
class Effect(Package):
    """Effect Package"""
    
    _ext = 'fx'
    _blend = 'effect.blend'
    _config = 'effect.json'
    _schema = 'Schemas/effect.json'
    _new = 'Schemas/effect_new.json'
    _dir = 'Effects'