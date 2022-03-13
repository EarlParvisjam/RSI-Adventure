from random import randrange
import utils, map

class Item():
    """Base class for all items"""
    def __init__(self, item):
        self.id = item["id"]
        self.name = item["name"]
        self.description = item["description"]
        self.value = item["value"]
        self.bound = item["bound"]
        if "container" in list(item.keys()) and item["container"] == True:
            self.container = True
            self.contents = item["contents"]
            self.status = "closed"
        else:
            self.container = False
            self.contents = None

    def __str__(self):
        if self.container and self.status == "opened":            
            return"{}(opened)\n========\n{}\nValue: {}\n".format(self.name, self.description, str(self.value))
        elif self.container and self.status == "closed":
            return "{}(closed)\n========\n{}\nValue: {}\n".format(self.name, self.description, str(self.value))
        else:
            return "{}\n========\n{}\nValue: {}\n".format(self.name, self.description, str(self.value))

    def quick_show(self):
        if self.container and self.status == "opened":
            return "{}(opened)\n".format(self.name)
        elif (self.container):
            return "{}(closed)\n".format(self.name)
        else:
            return self.name

    def remove(self):
        utils.cls()
        if self.container:
            print("Items: \n")
            for x in self.container:
                print(x.name + '(' + str(x.id) + ')')
            choice = input("\nRemove which item? ")
            print('\n')
            for item in container:
                if (str.isnumeric(choice) and choice == str(item.id)) or (choice.lower() == item.name.lower()): 
                    print("Removed {} from {}.".format(item.name, container.name))
                    input("\nHit any key to continue...")
                    return item
        input("\nHit any key to continue...")            
        return None

    def use(self):
        pass

class Weapon(Item):
    def __init__(self, weapon):
        super().__init__(weapon)
        self.damage = weapon["damage"]
        self.uses = weapon["uses"]
        self.slot = weapon["slot"]
        
    def attack(self):
        return self.uses[randrange(0, len(self.uses)-1)]

    def __str__(self):
        return "{}\n========\n{}\nValue: {}\nDamage: {}\n".format(self.name, self.description, self.value, self.damage)

class Gear(Item):
    def __init__(self, gear):
        super().__init__(gear)
        self.slot = gear["slot"]
        self.defense = gear["defense"]

    def __str__(self):
        return "{}\n========\n{}\nValue: {}\nSlot: {}\n".format(self.name, self.description, str(self.value), self.slot)

class Consumable(Item):
    def __init__(self, consumable):
        super().__init__(consumable)
        self.energy = consumable["energy"]
        self.caffeination = consumable["caffeination"]
        self.use = consumable["use"]

    def consume(self, player):
        player.energy += self.energy
        player.caffeination += self.caffeination
        if player.caffeination > 15:
            player.inventory.append(map.find_item(107))
            fresh_feeling = map.find_item(102)
            if fresh_feeling in player.inventory:
                player.inventory.remove(fresh_feeling)
        print(self.use)
        player.inventory.remove(self)

class Paper_Towel(Consumable):
    def __init__(self, paper_towel):
        super().__init__(paper_towel)
    
    def use(self, player):
        if map.find_item(109) in player.inventory:
            print(self.use)
            player.inventory.remove(self)
        else:
            print("\nYou really wish you had a paper towel right now, but you don't so I'm not sure what you're trying to accomplish.")

class Somebodys_Lunch(Consumable):
    def __init__(self, lunch):
        super().__init__(lunch)

    def use(self, player):
        print("\nHow could you?  That food wasn't yours.  Have you no shame?  Mark my words, this will haunt you for a long time...")
        player.inventory.remove(self)
        player.inventory.append(map.find_item(110))
