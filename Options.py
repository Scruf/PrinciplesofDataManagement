from Connection import Connection
from Character import Character
from Location import Location
from tabulate import tabulate
import Building
import Quest
import Loot

connection = Connection()
characterInst = Character()
locationInst = Location()


class Options:

	def __init__(self):
		self.connection = Connection()

	'''Puts the starting options out on the console, handles character creation/loading'''
	def start_options(self):
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

	        self.location_options(character_id, locName, locType, bldgTypes)

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

	            self.location_options(character_id, locName, locType, bldgTypes)
	        else:
	            print("Character not found! Returning to options...")
	            self.start_options()
	    elif start_str == "3":
	        self.game_outro()


	'''Handles selection when calling generic menu items (map, quests, etc...)'''
	def menu_option(self, option_str, player_id, loc_name, loc_type, building_types):
	    selection = option_str.lower()

	    if selection == 'm' or selection == 'map':
	        self.display_map(player_id, loc_name, loc_type, building_types)
	    elif selection == 'q' or selection == 'quest':
	        self.display_quest_log(player_id, loc_name, loc_type, building_types)
	    elif selection == 'i' or selection == 'inventory':
	        self.display_char_inventory(player_id, loc_name, loc_type, building_types)
	    elif selection == 'h' or selection == 'help':
	        self.game_help()
	        self.location_options(player_id, loc_name, loc_type, building_types)
	    elif selection == 'e' or selection == 'exit':
	        self.game_outro()
	    else:
	        print("Oops, you entered in a bad command!\n"
	              "I guess if you can't follow directions, you should stop playing :(")
	        self.game_outro()


	'''Provides options to do once in a location'''
	def location_options(self, player_id, loc_name, loc_type, building_types):
	    loc_inst = Location()
	    build_inst = Building.Building()
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
	            curr_name = characterInst.get_char_name(player_id)
	            loc_id = loc_inst.get_current_location(curr_name)
	            build_inst.enter_building(bldg_type, player_id, loc_id)
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
	                self.location_options(player_id, dest_name, destType, destBldgs)
	            else:
	                dest_name = loc_name
	                self.location_options(player_id, dest_name, loc_type, building_types)
	    except ValueError:
	        self.menu_option(selection, player_id, loc_name, loc_type, building_types)

	'''Displays map that character can go to'''
	def display_map(self, player_id, curr_loc_name, curr_loc_type, curr_building_types):
		player_locations = locationInst.map(player_id)

		player_map = "Enter location ID to travel to city, or enter 'C' to cancel\n"
		for index, location in enumerate(player_locations):
			city_name = location["city_name"]
			player_map += "{}) {}\n".format((index+1), city_name)
		print(player_map)

		map_selection = input("Selection: ")
		try:
			city_num = int(map_selection)
			if city_num <= len(player_locations):
				selected_city = player_locations[city_num - 1]
				selected_id = selected_city["city_id"]

				update_query = """CALL Test.update_location('{}','{}')""".format(
					selected_id, player_id
				)
				self.connection.cursor.execute(update_query)
				self.connection.conn.commit()

				character_name = characterInst.get_char_name(player_id)
				townObj = locationInst.get_location(character_name)

				locName = townObj["city_name"]
				locType = townObj["town_description"]
				bldgTypes = townObj["buildings"]

				print("blding types length: {}".format(len(bldgTypes)))
				if len(bldgTypes) > 0:
					self.location_options(player_id, locName, locType, bldgTypes)
				else:
					locationInst.populate(selected_id)
					self.location_options(player_id, locName, locType, bldgTypes)
		except ValueError:
			self.location_options(player_id, curr_loc_name, curr_loc_type, curr_building_types)

	'''Displays quest log for character'''
	def display_quest_log(self, player_id, loc_name, loc_type, building_types):
		quests = characterInst.fetch_quests(player_id)
		location_id = locationInst.get_location_id(loc_name)
		print("Choose Quest From Quest Log by ID: (Type 'C' to Cancel) \n")
		table = []

		for index, item in enumerate(quests):
			finished = ""
			if int(item['finished']) == 1:
				finished = "yes"

			table.append([(index+1), item['description'], item['reward'], finished])
		print (tabulate(table, headers=['ID',
										'Description',
										'Reward',
										'Completed?'
										]))

		choice = input("Select: ")
		try:
			choice_id = int(choice)
			if choice_id <= len(quests):
				quest_id = quests[choice_id - 1]['quest_id']
				questInst = Quest.Quest()
				questInst.initiate_quest(quest_id, player_id, location_id)
			else:
				print("Oops, that's not a quest you have!")
				self.display_quest_log(player_id, loc_name, loc_type, building_types)
		except ValueError:
			self.location_options(player_id, loc_name, loc_type, building_types)


	'''Displays inventory for character'''
	def display_char_inventory(self, player_id, loc_name, loc_type, building_types):
		characterInst = Character()
		loot = characterInst.fetch_loot(player_id)
		print("\nInventory (Type \"equip\" to begin equipping an item, \"C\" to Cancel')")
		i = 0
		table = []

		for item in loot:
			table.append([item['loot_id'],
							item['loot_name'],
							item['item_value'],
							item['item_desc'],
							item['equipped']])

		print (tabulate(table, headers=['ID',
										'Name',
										'Item Value',
										'Item Description',
										'Equipped']))
		choice = input("Select: ")
		if choice == 'C' or choice == 'c':
			self.location_options(player_id, loc_name, loc_type, building_types)
		elif choice == 'equip' or choice == 'Equip':
			while(True):
				lootInst = Loot.Loot()
				selection = input("Which item would you like to equip? (Type the ID) ")
				if selection == 'C':
					break
				loot_is_in = False
				for loot_item in loot:
					if int(selection) in loot_item.values():
						loot_is_in = True

				if loot_is_in == False:
					#player doesn't have that loot item
					print("You don't have that item!")
				else:
					selectLoot = lootInst.get_loot_item(selection)
					equippedLoot = lootInst.get_equipped_items(player_id)
					#if we already have the same type of item equipped,
					#unequip that item
					item_in_equipped = False
					for item in equippedLoot:
						if item['loot_type'] == selectLoot['loot_type']:
							lootInst.unequip_item(player_id, item['loot_id'], item['loot_type'])
							lootInst.equip_item(player_id, int(selection), selectLoot['loot_type'])
							print("{} equipped!\n".format(selectLoot['loot_name']))
							item_in_equipped = True
							break
					if item_in_equipped == True:
						break

					lootInst.equip_item(player_id, int(selection), selectLoot['loot_type'])
					print("{} equipped!\n".format(selectLoot['loot_name']))
					break

			self.location_options(player_id, loc_name, loc_type, building_types)
		self.location_options(player_id, loc_name, loc_type, building_types)

	'''Reads from text file, says goodbye and closes program'''
	def game_outro(self):
	    outro_file = open('goodbye.txt', 'r')
	    print(outro_file.read())
	    outro_file.close()

	    quit()

	'''Reads from help text file'''
	def game_help(self):
	    help_file = open('help.txt', 'r')
	    print(help_file.read())
	    help_file.close()


			
