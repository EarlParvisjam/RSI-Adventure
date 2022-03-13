import room, enemies, items, events
import json, sys

_map = {} 
_enemies = {}
_items = {}
_weapons = {}
_gear = {}
_consumable = {}

def load_data(map, bestiary, loadout):
    '''Parse enemies json file'''
    with open(bestiary, 'r') as f:
        rawBestiary = dict(json.load(f))["enemies"]
        for enemy in rawBestiary:
            load_enemy(enemy)
    '''Parse items json file'''
    with open(loadout, 'r') as f:
        rawItems = dict(json.load(f))
        for item in rawItems["items"]:
            load_item(item)
        for weapon in rawItems["weapons"]:
            _weapons[weapon["id"]] = items.Weapon(weapon)
        for armor in rawItems["gear"]:
            _gear[armor["id"]] = items.Gear(armor)
        for consumable in rawItems["consumable"]:
            _consumable[consumable["id"]] = items.Consumable(consumable)
    load_map(map)

def load_map(current_map):
    """Parse map json file"""
    if current_map == "resources/day1_map.json":
        with open(current_map, 'r') as f:
            rawMap = dict(json.load(f))["rooms"]
            for tile in rawMap:
                if (tile["id"]== 4):
                    _map[tile["id"]] = room.Kitchen(tile)  
                elif (tile["id"]==7):
                    _map[tile["id"]] = room.Main_Entrance(tile)  
                elif (tile["id"]==10):
                    _map[tile["id"]] = room.Break_Room(tile)
                elif (tile["id"]==11):
                    _map[tile["id"]] = room.Restrooms(tile)
                else:
                    _map[tile["id"]] = room.Tile(tile)  
    else:
        #load subsequent days into existing map
        with open(current_map, 'r') as f:
            rawMap = dict(json.load(f))["rooms"] 
            for tile in rawMap:
                pass

def load_enemy(enemy):
    """Custom enemy object construction"""
    if enemy["id"] == 50:
         _enemies[enemy["id"]] = enemies.Scrum(enemy)
    elif enemy["id"] == 59:
         _enemies[enemy["id"]] = enemies.Coffee_Station(enemy)
    else:
        _enemies[enemy["id"]] = enemies.Enemy(enemy)

def load_item(item):
    _items[item["id"]] = items.Item(item)

def load_consumable(consumable):
    if consumable["id"] == 204:
        _items[item["id"]] = items.Paper_Towel(consumable)
    elif consumable["id"] == 205:
        _items[item["id"]] = items.Somebodys_Lunch(consumable)
    else:
        _items[item["id"]] = items.Consumable(consumable)

def tile_exists(id):
    return _map.get(id)

def find_tile(id):
    return _map[id]

def find_enemy(id):
    return _enemies[id]

def find_item(id):
    return _items[id]

def find_weapon(id):
    return _weapons[id]

def find_gear(id):
    return _gear[id]

def find_consumable(id):
    return _consumable[id]

def find_thing(id):
    if id < 50:
        return find_tile(id)
    elif id < 100:
        return find_enemy(id)
    elif id < 200:
        return find_item(id)
    elif id < 500:
        return find_consumable(id)
    elif id < 1000:
        return find_gear(id)
    else:
        return find_weapon(id)

def return_type(id):
    if id < 50:
        return "location"
    elif id < 100:
        return "enemy"
    elif id < 500:
        return "item"
    elif id < 1000:
        return "gear"
    else:
        return "weapon"

def quit(self):
    sys.exit(0)

