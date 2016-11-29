from Connection import Connection
import json
from random import randint
from pprint import pprint
from Character import Character
from Dungeon import Dungeon
import Building

class NPC():

	def __init__(self):
		self.connection = Connection()

	"""
		@method get_npc will return a random npc from the npc.json
	"""
	def get_npc(self):
		npc_list = []
		
		with open('npc.json') as data:
			npc_list =  json.load(data)

		return npc_list[randint(0,len(npc_list))]

	def create_npc(self, player_id, typeStr, location_id):
		buildInst = Building.Building()
		with open('npc_names.json') as data:
			npc_names = json.load(data)

		random_npc= randint(0, len(npc_names) - 1)
		name = npc_names[random_npc]['name']

		if (typeStr == 'BlackSmith'):
			function = 'Blacksmith'
		elif(typeStr == 'Tavern'):
			function = 'Bartender'
		elif (typeStr == 'Church'):
			function = 'Priest'
		elif (typeStr == 'Potion Shop'):
			function = 'Potion Dealer'
		elif (typeStr == 'Armor Shop'):
			function = 'Armor Dealer'
		elif (typeStr == 'Defense Shop'):
			function = 'Defense Dealer'
		elif (typeStr == 'Inn'):
			function = 'Innkeeper'
		elif (typeStr == 'Clinic'):
			function = 'Healer'
		fullName = name + " the " + function

		self.connection.cursor.execute("""INSERT INTO `NPC`(npc_name, npc_function, location_id)
    									VALUES('{}', '{}', '{}');""".format(fullName, typeStr, location_id))
		self.connection.conn.commit()

		print("Upon entering the {} you see someone working hard.\n".format(typeStr))
		print("Options: \n")
		selection = input ("1) Approach them\n"
							"2) Leave\n"
							"Selection: ")
		if selection == "1":
			print("\"Hello, I'm {}. I've got a problem can you handle it?\"\n".format(fullName))
			choice = input("(Y/N) ")
			if choice == 'Y' or choice == 'y':
				#create quest
				description = self.create_quest(location_id, player_id)
				print("\"I need you to {}\"\n".format(description))
				print("Quest added to your quest log!")

			else:
				print("OK then out ya go!\n")

		buildInst.leave_building(player_id, location_id)
				



	"""
	@method creates a quest with the given location
	        id, and info about the character
	"""
	def create_quest(self, loc_id, player_id):
		dungeonInst = Dungeon()
		charInst = Character()
		level = charInst.get_char_level(18)
		dung_id = dungeonInst.create_dungeon(level, loc_id, player_id)
		reward = randint(50, 200)
		typeInt = randint(1, 3)
		#set the type
		if (typeInt == 1):
			typeChar = 'K'
			description = "Kill this monster"
		elif (typeInt == 2):
			typeChar = 'F'
			description = "Fetch an item for me"
		elif (typeInt == 3):
			typeChar = 'R'
			description = "Rescue my buddy"
		#set the experience
		if (level < 5):
			experience = randint(100, 800)
		else:
			experience = randint(1000, 3000)

		self.connection.cursor.execute("""CALL Test.create_quest('{}','{}', '{}', '{}', '{}', '{}')"""
									   .format(reward, description, typeChar, loc_id, experience, dung_id))
		self.connection.conn.commit()

		self.connection.cursor.execute("""SELECT quest_id FROM Quest WHERE Quest.dungeon_id = {}""".format(dung_id))

		quest_id = self.connection.cursor.fetchall()[0][0]

		self.connection.cursor.execute("""INSERT INTO Quest_log (character_id, quest_id) VALUES ({}, {})"""
										.format(player_id, quest_id))

		self.connection.conn.commit()

		return description




if __name__ == '__main__':
	npc =  NPC()
	pprint(npc.get_npc())
