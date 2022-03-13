
import items, map, utils, actions
from random import randrange

class Player():

    def __init__(self, mainWeapon, torso, legs, location):
        empty = map.find_item(100)
        self.inventory = []
        self.energy = 20
        self.caffeination = 0
        self.paper_towels = 0
        self.victory = False
        self.mainWeapon = mainWeapon
        self.offHand = empty
        self.wrist = empty
        self.fingers = empty
        self.torso = torso
        self.legs = legs
        self.feet = empty
        self.head = empty
        self.location = location


    def is_alive(self):
        return self.energy > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(action.source, action.method.__name__)
        if action_method:
            action_method(self, **kwargs)
        
    def acquire_loot(self, loot):
        self.inventory.append(loot)
        print(loot.name)
   
    def print_inventory(self):
        utils.cls()
        print("You have: ")
        if self.inventory:
            available_actions = []          
            for item in self.inventory:
                print(item.name)  
                #Manipulate inventory
                if item.container and not available_actions:
                    available_actions.append(Open())
                    break
                elif type(item) is items.Weapon or type(item) is items.Gear:
                    available_actions.append(actions.Equip(self))
                    break
            if len(self.inventory) > 0:
                available_actions.append(actions.Examine(None, self))
            print("\nAvailable actions:\n")
            for action in available_actions:
                print(action) 
            print("Enter: to return to previous menu")            
            action_input = input("\nChoice: ")
            for action in available_actions:
                if str(action_input).lower() == str(action.hotkey).lower():
                    self.do_action(action, **action.kwargs)
                    break
        else:
            print("\nNothing, lots of nothing")      

    def show_status(self):
        print("""
Energy: {}    Caffeination: {}  Paper Towels: {}
Head:      {}
Wrist:     {}
Fingers:   {}
Main hand: {}
Off-hand:  {}
Torso:     {}
Legs:      {}
Feet:      {}
""".format(self.energy, self.caffeination, self.paper_towels, self.head.name, self.wrist.name, 
            self.fingers.name, self.mainWeapon.name, self.offHand.name, self.torso.name, self.legs.name, self.feet.name))

    def calculate_defense(self):
        defense = 0
        if type(self.offHand) is items.Gear:
            defense += self.offHand.defense
        if type(self.fingers) is items.Gear:
            defense += self.fingers.defense
        if type(self.fingers) is items.Gear:
            defense += self.torso.defense
        if type(self.legs) is items.Gear:
            defense += self.legs.defense
        if type(self.feet) is items.Gear:
            defense += self.feet.defense
        if type(self.head) is items.Gear:
            defense += self.head.defense
        if type(self.wrist) is items.Gear:
            defense += self.wrist.defense
        return defense
    
    def calculate_combat(self):
        attack = randrange(0, 4) + self.mainWeapon.damage
        fresh_feeling = map.find_item(102)
        if fresh_feeling in self.inventory:  
            attack += fresh_feeling.value
        guilt = map.find_item(110)
        if guilt in self.inventory:
            attack -= guilt.value
        return attack