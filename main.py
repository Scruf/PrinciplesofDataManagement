from Connection import Connection
from Character import Character
from Location import Location

connection = Connection()
characterInst = Character()
locationInst = Location()

'''Reads from text file, greets the player'''
def game_intro():
    intro_file = open('welcome.txt', 'r')
    print(intro_file.read())
    intro_file.close()
    start_options()

'''Reads from text file, says goodbye and closes program'''
def game_outro():
    outro_file = open('goodbye.txt', 'r')
    print(outro_file.read())
    outro_file.close()

    quit()

'''Reads from help text file'''
def game_help():
    help_file = open('help.txt', 'r')
    print(help_file.read())
    help_file.close()

'''Puts the starting options out on the console, handles character creation/loading'''
def start_options():
    start_str = input("1) Create New Character\n"
                      "2) Load Character\n"
                      "3) Exit\n"
                      "Selection: ")

    if start_str == "1":
        character_name = input("Enter Character Name (30 character limit): ")
        characterInst.create_character(character_name)
        character_id = characterInst.get_char_id(character_name)

        townObj = locationInst.get_location(character_name)

        locName = townObj["city_name"]
        locType = townObj["town_description"]
        bldgTypes = townObj["buildings"]

        location_options(character_id, locName, locType, bldgTypes)

    elif start_str == "2":
        characters = characterInst.fetch_characters()
        for character in characters:
            print("\t" + character)
        character_name = input("Enter Character Name: ")
        if character_name in characters:
            print("Loading character...\n")
            character_id = characterInst.get_char_id(character_name)

            townObj = locationInst.get_location(character_name)

            locName = townObj["city_name"]
            locType = townObj["town_description"]
            bldgTypes = townObj["buildings"]

            location_options(character_id, locName, locType, bldgTypes)
        else:
            print("Character not found! Returning to options...")
            start_options()
    elif start_str == "3":
        game_outro()


'''Handles selection when calling generic menu items (map, quests, etc...)'''
def menu_option(option_str, player_id, loc_name, loc_type, building_types):
    selection = option_str.lower()

    if selection == 'm' or selection == 'map':
        print("Selected map option")
    elif selection == 'q' or selection == 'quest':
        print("Selected quest log option")
    elif selection == 'i' or selection == 'inventory':
        print("Selected character inventory")
    elif selection == 'h' or selection == 'help':
        game_help()
        location_options(player_id, loc_name, loc_type, building_types)
    elif selection == 'e' or selection == 'exit':
        game_outro()
    else:
        print("Oops, you entered in a bad command!\n"
              "I guess if you can't follow directions, you should stop playing :(")
        game_outro()


'''Provides options to do once in a location'''
def location_options(player_id, loc_name, loc_type, building_types):
    loc_inst = Location()
    desc_str = "You find yourself in the {} of {}.\nYou see".format(loc_type, loc_name)
    opts_str = "[(M)ap] [(Q)uest] [(I)nventory] [(H)elp] [(E)xit]\n"

    for index, building_type in enumerate(building_types):
        if index < (len(building_types) - 1):
            desc_str += " a {},".format(building_type)
        elif index == (len(building_types) - 1):
            desc_str += " and a {}.\nWhat do you do?\n".format(building_type)

        opts_str += "{}) Go to {}\n".format((index + 1), building_type)

    opts_str += "{}) Leave {}\n".format((len(building_types)+1), loc_name)

    print(desc_str)
    print(opts_str)

    selection = input("Selection: ")
    try:
        select_num = int(selection)
        if select_num <= len(building_types):
            bldg_type = building_types[select_num-1]
            #TODO Go to bldg_type (like "Blacksmith")

        else:
            print("Leaving {}".format(loc_name))
            nearby_towns = loc_inst.leave(player_id, False)
            nearby_str = "[(M)ap] [(Q)uest] [(I)nventory] [(H)elp] [(E)xit]\n"

            for index, town in enumerate(nearby_towns):
                town_name = town["city_name"]
                nearby_str += "{}) Go to {}\n".format((index + 1), town_name)
            nearby_str += "{}) Head back into {}\n".format((len(nearby_towns) + 1), loc_name)
            print(nearby_str)

            travel_str = input("Selection: ")
            selection = travel_str
            travel_id = int(travel_str)
            if travel_id <= len(nearby_towns):
                dest_name = nearby_towns[travel_id-1]["city_name"]

                dest_obj = locationInst.go_to(dest_name, player_id)
                destType = dest_obj["town_description"]
                destBldgs = dest_obj["buildings"]
                location_options(player_id, dest_name, destType, destBldgs)
            else:
                dest_name = loc_name
                location_options(player_id, dest_name, loc_type, building_types)
    except ValueError:
        menu_option(selection, player_id, loc_name, loc_type, building_types)

game_intro()

