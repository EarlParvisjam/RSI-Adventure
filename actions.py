import map, items, utils

class Action():
    def __init__(self, source, method, name, hotkey, **kwargs):
        self.method = method
        self.source = source
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs
    
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)

class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self, player):
        super().__init__(source = ViewInventory, method = self.print_inventory, name = "Inventory", hotkey='i', player = player)

    def print_inventory(self, player):
        player.print_inventory()
        input("\nHit any key to continue...")

class Status(Action):
    """Prints the player's status"""
    def __init__(self, player):
        super().__init__(source = Status, method = self.show_status, name = "Status", hotkey='z', player = player)

    def show_status(self, player):
        player.show_status()
        input("\nHit any key to continue...")

class Attack(Action):
    def __init__(self, player, target):
        super().__init__(source = Attack, method = self.attack, name = "Attack", hotkey='a', player = player, target = target)

    def attack(self, player, target):
        if player.location.enemies:
            if not target:
                utils.cls()
                print(player.location.look_enemies())
                enemy = input("\nWhich challenge would you like to deal with? ")
            else:
                enemy = str(target.id)
            for i in player.location.enemies:
                temp = str.isnumeric(enemy)
                if (str.isnumeric(enemy) and enemy == str(i.id)) or (enemy.lower() == i.name.lower()):
                    print('\nYou address the problem:\n' + player.mainWeapon.attack())
                    i.hp -= player.calculate_combat()
                    i.aggressive = True
                    if i.is_alive():
                        player.energy -= i.calculate_attack(player.calculate_defense())
                        print('\n{} responds:\n{}\n'.format(i.name,i.attack()))
                        input("\nHit any key to continue...")
                    else:
                        utils.cls()
                        i.death_trigger(player)
                        i.get_loot(player)
                        player.location.enemies.remove(i)
                        input("\nHit any key to continue...")

class Quit(Action):
    def __init__(self):
        super().__init__(source = map, method = map.quit, name = "Quit", hotkey='q')

class Open(Action):
    def __init__(self, container):
        super().__init__(source = Open, method = self.open, name = "Open", hotkey='o', container = container)

    def open(self, container):
        utils.cls()
        if container.status == "closed":
            print("Opening {}.".format(container.name))
            container.status = "opened"
        else:
            print ("{} is already opened.".format(container.name))
            container.status = "opened"

class Close(Action):
    def __init__(self, container):
        super().__init__(source = Close, method = self.close, name = "Close", hotkey='c', container = container)

    def close(self, container):
        utils.cls()
        if container.status == "opened":
            print("Closing {}.".format(container.name))
            container.status = "closed"
        else:
            print ("{} is already closed.".format(container.name))
            container.status = "closed"

class Get(Action):
    def __init__(self, container, player):
        super().__init__(source = Get, method = self.get, name = "Get", hotkey='g', container = container, player = player)

    def get(self, container, player):
        utils.cls()
        print("\nItems: ")
        for item in container:
            #item = map.find_thing(i)
            if not item.bound:
                print(item.name + '(' + str(item.id) + ')')

        acquire = input("Which would you like to acquire? ")
        utils.cls()
        for thing in container:   
            if (str.isnumeric(acquire) and acquire == str(thing.id)) or (acquire.lower() == thing.name.lower()): 
                player.inventory.append(thing)
                container.remove(item)
                print("\nYou put the {} in your inventory.\n".format(thing.name))
                input("\nHit any key to continue...")


class Put(Action):
    def __init__(self, container, player):
        super().__init__(source=Put, method = self.put, name = "Put", hotkey='p', container = container, player = player)

    def put(self, contianer, player):
        utils.cls()
        print("\nItems: ")
        for item in player.inventory:
            if not item.bound:
                print(item.name + '(' + str(item.id) + ')')
        acquire = input("Which would you like to acquire? ")
        utils.cls()
        for thing in player.inventory:   
            if (str.isnumeric(acquire) and acquire == str(thing.id)) or (acquire.lower() == thing.name.lower()): 
                container.items.append(thing)
                player.inventory.remove(item)
                print("\nYou put {} in {}.\n".format(thing.name, container.name))
                input("\nHit any key to continue...")

class Examine(Action):
    def __init__(self, tile, player):
        super().__init__(source = Examine, method = self.examine, name = "Examine", hotkey='x', tile = tile, player = player)

    def examine(self, tile, player):
        utils.cls()
        options = []
        if tile:
            if tile.items or tile.enemies:
                print ("Challenges:\n")
                for x in tile.enemies:
                    print (x.name + '(' + str(x.id) + ')')
                print("\nItems: \n")
                for x in tile.items:
                    print(x.name + '(' + str(x.id) + ')')
                choice = input("\nExamine which thing? ")
                utils.cls()
                print('\n')
                for enemy in tile.enemies:
                    if (str.isnumeric(choice) and choice == str(enemy.id)) or (choice.lower() == enemy.name.lower()): 
                        print(str(enemy))
                        options.append(Attack(player, enemy))
                        break
                [options.append(x) for x in examine_items(tile.items, choice, player)]
        else:
            print("\nItems: \n")
            for x in player.inventory:
                print(x.name + '(' + str(x.id) + ')')
            choice = input("\nExamine which thing? ")
            utils.cls()
            print('\n')
            options = examine_items(player.inventory, choice, player)
            
        if options:
            for action in options:
                print(action)     
            print("Enter: to return to previous menu")       
            action_input = input("\nChoice: ")
            for action in options:
                if str(action_input).lower() == str(action.hotkey).lower():
                    player.do_action(action, **action.kwargs)
                    break

class Remove(Action):
    def __init__(self, container, player):
        super().__init__(source = Remove, method = self.remove, name = "Remove", hotkey='r', container = container, player = player)

    def remove(self, container, player):
        utils.cls()
        if container:
            print("Items: \n")
            for x in container:
                print(x.name + '(' + str(x.id) + ')')
            choice = input("\nRemove which item? ")
            utils.cls()
            print('\n')
            for item in container:
                if (str.isnumeric(choice) and choice == str(item.id)) or (choice.lower() == item.name.lower()): 
                    list(container).remove(item)
                    list(player.inventory).append(item)
                    break
        
        input("\nHit any key to continue...")

class Equip(Action):
    def __init__(self, player):
        super().__init__(source = Equip, method = self.equip, name = "Equip", hotkey='d', player = player)

    def equip(self, player):
        empty = map.find_item(100)
        for x in player.inventory:
                print(x.name + '(' + str(x.id) + ')') 
        id = input("\nWhich would you like to equip? ")
        for item in player.inventory:
            if (str.isnumeric(id) and id == str(item.id)) or (id.lower() == item.name.lower()): 
                player.inventory.remove(item)
                if type(item) is items.Weapon:
                    if map.find_item(109) not in player.inventory:  #Check for Wet Hands
                        if item.slot == "main":
                            if not player.mainWeapon == map.find_weapon(1003):
                                player.inventory.append(player.mainWeapon)
                            player.mainWeapon = item
                            break
                        else:
                            player.inventory.append(player.offHand)
                            player.offHand = item
                            break
                    else:
                        print("\nYour hands are just too wet and slippery to hold the {}.\n".format(item.name))
                        player.inventory.append(item)
                        break
                print("\nYou equip the {}.\n".format(item.name))
                if type(item) is items.Gear:
                    if item.slot == "wrist":
                        if not player.wrist == empty:
                            player.inventory.append(player.wrist)
                        player.wrist = item
                        break
                    elif item.slot == "fingers":
                        if not player.wrist == empty:
                            player.inventory.append(player.fingers)
                        player.fingers = item
                        break
                    elif item.slot == "torso":
                        if not player.wrist == empty:
                            player.inventory.append(player.torso)
                        player.torso = item
                        break
                    elif item.slot == "legs":
                        if not player.wrist == empty:
                            player.inventory.append(player.legs)
                        player.legs = item
                        break
                    elif item.slot == "feet":
                        if not player.wrist == empty:
                            player.inventory.append(player.feet)
                        player.feet = item
                        break
                    elif item.slot == "head":
                        if not player.wrist == empty:
                            player.inventory.append(player.head)
                        player.head = item
                        break
                    else:
                        print("This item is for a gear slot I don't understand.")
                        break
                else:
                    print("{} can not be equipped.".format(item.name))
                    break
        input("\nHit any key to continue...")

class Use(Action):
    def __init__(self, item, player):
        super().__init__(source = Use, method = self.use, name = "Use", hotkey='u', item = item, player = player)

    def use(self, item, player):
        utils.cls()
        if isinstance(item, items.Consumable): 
            item.consume(player)

def examine_items(things, choice, character):
    options = []
    for item in things:
        if (str.isnumeric(choice) and choice == str(item.id)) or (choice.lower() == item.name.lower()): 
            if item.container and item.status == "closed":
                print(str(item))
                options.append(Open(item))
            elif item.container:
                print(str(item) + '\nContains:')
                if item.container:
                    for val in item.contents:
                        thing = map.find_thing(val)
                        print(thing.name + '(' + str(thing.id) + ')')
                    if item.contents:
                        options.append(Get(item.contents, character))
                    options.append(Close(item))
                    print(" ")
            else:
                print(str(item))
                if type(item) is items.Consumable:
                    options.append(Use(item, character))
            break
    return options

