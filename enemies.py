from random import randrange
import map

class Enemy:
    
    def __init__(self, enemy):
        self.id = enemy["id"]
        self.name = enemy["name"]
        self.description = enemy["description"]
        self.armor = enemy["armor"]
        self.hp = enemy["hp"]
        self.damage = enemy["damage"]
        self.attacks = enemy["attacks"]
        self.death = enemy["death"]
        self.loot = enemy["loot"]
        self.aggressive = enemy["aggressive"]

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        return self.attacks[randrange(0, len(self.attacks)-1)]

    def calculate_attack(self, defense):
        damage = randrange(0, 4) + self.damage
        if damage < defense:
            print("\n**Wow, rather than sapping your will to live, wearing your gear helps you feel oddly energized.  Nothing can stop you.**")
        return randrange(0, 4) + self.damage - defense

    def death_trigger(self, player):
        print('\n' + self.death + '\n')

    def quick_show(self):
        if self.aggressive:
            hostile = "*"
        else:
            hostile = ""
        return "{}{}({})".format(hostile, self.name, str(self.id))

    def __str__(self):
        if self.aggressive:
            hostile = "*"
        else:
            hostile = ''
        return "{}{}({})\n========\n{}\n".format(hostile, self.name, str(self.id), self.description)
    
    def get_loot(self, player):        
        if self.loot:
            for i in self.loot:
                item = map.find_thing(i)
                print("\nFor resisting {}, you are rewarded with:".format(item.name))
                player.acquire_loot(item)

class Scrum(Enemy):
    def __init__(self, enemy):
        super().__init__(enemy)
        
    def death_trigger(self, player):
        super().death_trigger(player)
        player.location.enemies.append(map.find_enemy(56))

class Coffee_Station(Enemy):
    def __init__(self, enemy):
        super().__init__(enemy)

    def get_loot(self, player):
        super().get_loot(player)
        player.paper_towels += 1
        