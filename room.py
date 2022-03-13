import game
import map, items, enemies, actions, actions_move, actions_custom, events, utils

class Tile:
    def __init__(self, tile):
        self.name = tile["name"]
        self.description = tile["description"]
        self.enemies = self.create_enemies(tile["enemies"])
        self.items = self.create_items(tile["items"])
        self.neighbors = tile["neighbors"]

    def available_actions(self, character):
        """Returns all available actions in this room."""
        options = []    
        if self.check_hostiles():
            print("\nYou have Challenges (*) that you can't ignore right now.\n")
            options.append(actions.Attack(character, None))
        elif self.enemies:
            options = self.available_moves(character)
            options.append(actions.Attack(character, None))
        else:
            options = self.available_moves(character)
        for item in self.items:
            if not item.bound:
                options.append(actions.Get(self.items, character))
                break
        for item in self.items:
            if isinstance(item, items.Consumable):
                options.append(actions.Use(item, character))
                break
        if character.paper_towels > 0 and map.find_item(109): 
            options.append(actions.Dry_Hands(self, character)) #Add Dry Hands if towels are available
        if self.items or self.enemies:
            options.append(actions.Examine(self, character))
        options.append(actions.ViewInventory(character))
        return options

    def available_moves(self, character):
        options = []
        for id, tile in self.neighbors.items():
            if id == 'n':
                options.append(actions_move.MoveNorth(character))
            elif id == 's':
                options.append(actions_move.MoveSouth(character))
            elif id == 'e':
                options.append(actions_move.MoveEast(character))
            elif id == 'w':
                options.append(actions_move.MoveWest(character))
            elif id == 'drive':
                options.append(actions_move.Drive(character))
        return options

    def intro_text(self):
        return "{}\n\n{}\n{}".format(self.description, self.look_enemies(), self.look_items())

    def create_enemies(self, numbers):
        targets = []
        if numbers:
            for id in numbers:
                targets.append(map.find_enemy(id))
        return targets

    def create_items(self, numbers):
        targets = []
        if numbers:
            for id in numbers:
                targets.append(map.find_thing(id))
        return targets

    def look_enemies(self):
        if self.enemies:
            return "Challenges: \n" + ('\n'.join([x.quick_show() for x in self.enemies])) + '\n'
        return "Challenges: \n"

    def look_items(self):
        if self.items:
            return "Items:\n"  + ('\n'.join([x.quick_show() for x in self.items]))
        return "Items:\n"

    def check_hostiles(self):
        for x in self.enemies:
            if x.aggressive:
                return True
        return False
                      
    def enter_room(self, character):
        pass

class Kitchen(Tile):
    def __init__(self, tile):
        super().__init__(tile)  
        
    def available_actions(self, character):
        return super().available_actions(character)

    def enter_room(self, character):
        if  map.find_thing(201) not in character.inventory and not map.find_enemy(53) in self.enemies:
            events.Event.create_monster(self, 53) #Generate A Stove
        if game.day == "Tuesday" and not map.find_enemy(53).is_alive():
            events.Event.put_item(self, map.find_item(103), 202) #Put Leftovers into refrigerator

class Main_Entrance(Tile):
    def __init__(self, tile):
        super().__init__(tile)
    
    def available_actions(self, character):
        commands = super().available_actions(character)
        if 'n' not in character.location.neighbors:
            commands.append(actions_custom.Unlock(character))           
        return commands

    def available_moves(self, character):
        options = super().available_moves(character)
        if not map.find_enemy(54).is_alive():
            if 'n' not in self.neighbors:
                self.neighbors['n'] = 8 #Path to Print Shop
                options.append(actions_move.MoveNorth(character))
        if game.time == "lunch" and 'drive' not in list(self.neighbors.keys()):
            options.append(actions_move.Eat_Out(character))
        return options

    def intro_text(self):
        return super().intro_text()

class Break_Room(Tile):
    def __init__(self, tile):
        super().__init__(tile)  
        
    def available_actions(self, character):
        actions = super().available_actions(character)
        actions.append(actions_custom.Brew(character))
        if map.find_consumable(202) in character.inventory:
            actions.append(action.put(character, ))
        return actions

    def intro_text(self):
        '''Do something custom'''
        return super().intro_text()

class Your_Cube(Tile):
    def __init__(self, tile):
        super().__init__(tile)  
        self.enemies.append(enemies.Scrum(map.find_enemy(50), self))

    def available_actions(self, character):
        actions = super().available_actions(character)
        return actions

    def intro_text(self):
        #Verify Morning Scrum and Project Work are defeated
        if not map.find_enemy(50) not in self.enemies and map.find_enemy(56) not in self.enemies:
            if game.time == "morning":
                events.trigger_lunch()
            elif game.time == "afternoon":
                events.trigger_evening()
        return super().intro_text()

class Restrooms(Tile):
    def __init__(self, tile):
        super().__init__(tile)

    def available_actions(self, character):
        actions = super().available_actions(character)
        if map.find_item(107) in character.inventory:
            actions.append(actions_custom.Use_Bathroom(character))
        return actions

    def intro_text(self):
        '''Do something custom'''
        return super().intro_text()

class Blind_Mule(Tile):
    def __init__(self, tile):
        super().__init__(tile)

    def intro_text(self):
        staff = map.find_enemy(57)
        if staff not in self.enemies and game.time == "lunch":
            events.trigger_afternoon()
        return super().intro_text()         