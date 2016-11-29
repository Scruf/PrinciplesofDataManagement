from Connection import Connection
from Options import Options
from Character import Character
from NPC import NPC
from Location import Location
import json
from random import randint
from pprint import pprint

optionsInst = Options()

class Building():

	def __init__(self):
		pass

	def load_npcs(self, build_id):
		typ = self.connection.cursor.execute("""
			SELECT Type FROM Test.Building
			WHERE Test.Building. == %s 
			""", loc_id)

	def enter_building(self, build_type, player_id, location_id):
		npcInst = NPC()
		print("You enter the {}\n".format(build_type))
		npcInst.create_npc(player_id, build_type, location_id)

	def leave_building(self, player_id, location_id):
		characterInst = Character()
		locInst = Location()
		charName = characterInst.get_char_name(player_id)
		townObj = locInst.get_location(charName)
		optionsInst.location_options(player_id, townObj["city_name"], 
									townObj["town_description"], 
									townObj["buildings"])

if __name__ == '__main__':
	building = Building()