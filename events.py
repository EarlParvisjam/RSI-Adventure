import game, map, items
import copy

class Event():
    def __init__(self, room, method, **kwargs):
        self.room = room
        self.name = name
        self.method = method
        self.hotkey = hotkey
        self.kwargs = kwargs

    def create_item(self, room, id):
        item = deepcopy(map.find_thing(id))
        return item

    def create_inventory_item(self, id):
        item = deepcopy(map.find_thing(id))
        list(game.character.inventory).append(item)

    def create_monster(self, room, id):
        monster = copy.deepcopy(map.find_monster(id))
        list(room.enemies).append(monster)

    def remove_monster(self, room, id):
        for monster in room.enemies:
            if monster.id == id:
                list(room.enemies).remove(monster)
    
    def put_item(self, room, container, id):
        item = map.find_thing(id)
        list(room.items).remove(item)
        container.contents.append(item)

def trigger_lunch(self):
    game.time = "lunch"
    entrance = self.find_tile(7)
    if 'e' not in entrance.neighbors:
        entrance.neighbors['e'] = 12 #Add to The Blind Mule
    

def trigger_afternoon(self):
    game.time = "afternoon"
    if 'e' in entrance.neighbors:
        entrance.neighbors.pop('e') #remove path to Blind Mule
    your_cube = map.find_tile(9)
    wait_around = map.find_enemy(54)
    wait_around.hp = 10  #reactivate Wait Around challenge
    project_work = map.find_enemy(56)
    project_work.hp = 10  
    your_cube.enemies.append(project_work) #Reactivate Project Work
    foos = map.find_enemy(58)
    foos.hp = 20  
    map.find_tile(10).enemies.append()  #Add Foosball!!! to the Break Room

    
def trigger_evening(self):
    game.time = "evening"
    parking_lot = map.find_tile(6)
    if 'drive' not in parking_lot.neighbors:
        pass
    
def trigger_new_day(self):
    work_fridges = map.find_item(105)
    leftovers = map.find_consumable(202)
    rotten_food = map.find_item(111)
    if leftovers in work_fridges:
        work_fridges.append(rotten_food)
        work_fridges.remove(leftovers)
