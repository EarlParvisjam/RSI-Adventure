from actions import Action
import game, map, utils

class MoveNorth(Action):
    def __init__(self, player):
        super().__init__(source = MoveNorth, method = self.move_north, name = 'Move north', hotkey='n', player = player)

    def move_north(self, player):      
        player.location = map.tile_exists(player.location.neighbors['n'])
        player.location.enter_room(player)

class MoveSouth(Action):
    def __init__(self, player):
        super().__init__(source = MoveSouth, method = self.move_south, name = 'Move south', hotkey='s', player = player)

    def move_south(self, player):      
        player.location = map.tile_exists(player.location.neighbors['s'])
        player.location.enter_room(player)

class MoveEast(Action):
    def __init__(self, player):
        super().__init__(source = MoveEast, method = self.move_east, name = 'Move east', hotkey='e', player = player)

    def move_east(self, player):      
        player.location = map.tile_exists(player.location.neighbors['e'])
        player.location.enter_room(player)

class MoveWest(Action):
    def __init__(self, player):
        super().__init__(source = MoveWest, method = self.move_west, name = 'Move west', hotkey='w', player = player)

    def move_west(self, player):      
        player.location = map.tile_exists(player.location.neighbors['w'])
        player.location.enter_room(player)

class Drive(Action):
    def __init__(self, player):
        super().__init__(source = Drive, method = self.drive, name = "Drive to Work", hotkey='drive', player = player)

    def drive(self, player):
        utils.cls()
        print("You get in your transportation and head for work.  There's no going back now.  Thankfully, traffic isn't bad and nobody tries to run you off the road.\n")
        if map.find_item(103).status == "open":
                print("\nHalf way to work, you remember that you left your fridge open.\n")      
        if map.find_consumable(201) in player.inventory:
            print("You hop out and start to gather your things.  You realize that the breakfast you spent so much effort to make has spilled all over the passenger seat.")
            player.inventory.remove(map.find_consumable(201))
        player.location = map.tile_exists(6)
        player.location.enter_room(player)
        input("\nHit any key to continue...")

class Eat_Out(Action):
    def __init__(self, player):
        super().__init__(source=Eat_Out, method = self.eat_out, name = "Go Out For Lunch", hotkey='drive', player = player)

    def eat_out(self, player):
        utils.cls()
        print("You opt to go out for lunch.  It's nice to get out of the office for a bit and you feel refreshed from the experience.\n")
        if 'e' in list(player.location.neighbors.keys()):
            player.location.neighbors.pop('e')
        game.time = "afternoon"
        player.energy += 10
        print("You gain 10 energy as a result.  Now you can better take on work.")
        input("\nHit any key to continue...")