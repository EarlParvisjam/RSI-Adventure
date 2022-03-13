from actions import Action
import map, utils

class Unlock(Action):
    def __init__(self, player):
        super().__init__(source = Unlock, method = self.unlock, name = "Unlock", hotkey='u', player = player)

    def unlock(self, player):
        item = map.find_thing(108)
        if  item in player.inventory:
            utils.cls()
            print("\nYou pull the {} from your pocket and wave it in front of a sensor bar by the door.  The door unlocks.".format(item.name))
            player.location.neighbors['n'] = 8
            input("\nHit any key to continue...")
        else:
            utils.cls()
            print("Feeling around in your pockets, you remember that you left the door fob in your bedroom.  Hopefully,\n someone will show up soon and let you in.")
            input("\nHit any key to continue...")
            if map.find_enemy(54) not in player.location.enemies:
                player.location.enemies.append(map.find_enemy(54))

class Brew(Action):
    def __init__(self, player):
        super().__init__(source = Brew, method = self.brew, name = 'Brew Keurig', hotkey='b', player = player)

    def brew(self, player):  
        utils.cls()
        item = map.find_consumable(200)
        if not item in player.inventory:
            print("\nYou partake of the bounty of the office.  {} is added to your inventory.".format(item.name))
            player.inventory.append(item)
        else:
            print("You stop yourself from pouring a cup of coffee, remembering that you already have one.")
        input("\nHit any key to continue...")

class Use_Bathroom(Action):
    def __init__(self, player):
        super().__init__(source = Use_Bathroom, method = self.go_potty, name = "Use Restroom", hotkey='p', player = player)
    
    def go_potty(self, player):
        utils.cls()
        over_caffeinated = map.find_item(107)
        if not item in player.inventory:
            print("\nYou don't really need to go right now.")
        else:
            print("\nYou avail yourself of the facilities.  No, I'm not going to say more about it than that.  This isn't THAT sort of game...")
            empty = map.find_item(100)
            player.inventory.remove(over_caffeinated)
            player.inventory.append(109) #Add wet hands to inventory
            if not player.mainWeapon == empty:
                player.inventory.append(player.mainWeapon)
                player.mainWeapon = empty
            if not player.offHand == empty:
                player.inventory.append(player.offHand)
                player.offHand = empty

        input("\nHit any key to continue...")

        