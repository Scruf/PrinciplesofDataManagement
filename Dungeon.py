from Connection import Connection
from pprint import pprint
import json
from random import randint


class Dungeon():


	def __init__(self):
		self.connection = Connection()
	"""
		@method create_dungeon will generate a dungeon based on the 
				player's level
		@param player_level is the player name
	"""

	def create_dungeon(self,level):
		with open('dungeon.json') as data:
			dungeon_names = json.load(data)

		random_dungeon = randint(0,len(dungeon_names)-1)
		dungeon_obj = {
			'name':dungeon_names[random_dungeon]['name'],
			'difficulty_level':level
		}
		self.connection.cursor.execute("""CALL Test.create_dungeon('{}','{}')"""
										.format(dungeon_obj['difficulty_level']
												,dungeon_obj['name']))
		


		self.connection.conn.commit()

	



if __name__ == '__main__':
	dungeon = Dungeon()
	dungeon.create_dungeon(3)