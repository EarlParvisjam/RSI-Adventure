
import map, player, utils, actions

day = "Monday"
time = "morning"

def pick_map():
    if day == "Monday":
        map = "resources/day1_map.json"
    else:
        map = "resources/day2_map.json"
    return map

def Play():
    map.load_data(pick_map(), "resources/enemies.json", "resources/items.json")
    character = player.Player(map.find_weapon(1003), map.find_gear(500), map.find_gear(501), map.find_tile(1))
    utils.cls()
    print('''
        Good Morning!
        It's {} and time to get ready for work.'''.format(day))
    input("\nHit any key to continue...")
    utils.cls()
    print("\n{}\t\t\t\t\t\t\tEnergy: {}\tPaper Towels: {}\n\n{}\n----------".format(character.location.name, character.energy, character.paper_towels, character.location.intro_text()))
    while character.is_alive() and not character.victory:
        print("Choose an action:")
        available_actions = character.location.available_actions(character)
        available_actions.append(actions.Status(character))
        available_actions.append(actions.Quit())
        for action in available_actions:
            print(action)            
        action_input = input("\nChoice: ")
        for action in available_actions:
            if str(action_input).lower() == str(action.hotkey).lower():
                character.do_action(action, **action.kwargs)
                break
        utils.cls()        
        print("\n{}\t\t\t\t\t\t\tEnergy: {}\tPaper Towels: {}\n\n{}\n----------".format(character.location.name, character.energy, character.paper_towels, character.location.intro_text()))
    utils.cls()
    if character.is_alive() and character.victory:
        print("\nSomehow, against all odds, you survived the week and came out a bit ahead.  Have a cookie.")
    elif character.is_alive():
        print("\nWell, that week could have gone a lot better.  At least you survived.")
    else:
        print("\nAt long last, your energy fully drained, you give up on this week.  No amount of coffee is going to perk you back up...")
    print(str(character.is_alive()) + " " + str(character.victory))

if __name__ == "__main__":
    Play()
    
