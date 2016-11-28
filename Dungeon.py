from Connection import Connection
from pprint import pprint
import json
from random import randint


class Dungeon:

	def __init__(self):
		self.connection = Connection()


	#Gets list of dungeons currently in DB
	def get_dungeons(self):
		self.connection.cursor.execute("""SELECT dungeon_name, difficulty_level FROM Dungeon;""")
		self.connection.conn.commit()

		key_list = []
		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		results = []
		for data in self.connection.cursor.fetchall():
			dictionary = dict(zip(key_list, list(data)))
			results.append(dictionary)

		return results

	def get_dungeon(self, name):
		self.connection.cursor.execute(
			"""SELECT dungeon_name, difficulty_level FROM Dungeon WHERE dungeon_name = '{}'""".format(
				name))
		key_list = []
		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		return dict(zip(key_list, list(self.connection.cursor.fetchall()[0])))
	"""
			@method create_dungeon will generate a dungeon based on the
					player's level
			@param player_level is the player name
	"""

	def create_dungeon(self, level, originId, playerId):
		with open('dungeon_names.json') as data:
			dungeon_names = json.load(data)

		random_dungeon = randint(0, len(dungeon_names) - 1)
		dungeon_name = dungeon_names[random_dungeon]['name']

		monsters = randint(2, 8)
		location_obj = {
			'loc_name': dungeon_name,
			'loc_limit': monsters,
			'loc_type': "Dungeon",
			'discovered_from_id': originId,
			'char_id': playerId
		}

		self.connection.cursor.execute("""CALL Test.add_location('{}', '{}', '{}', '{}', '{}')"""
									   .format(location_obj['loc_name'], location_obj['loc_limit'], location_obj['loc_type'], location_obj['discovered_from_id'], location_obj['char_id'])
									   )
		self.connection.conn.commit()

		dungeon_obj = {
			'name': dungeon_names[random_dungeon]['name'],
			'difficulty_level': level
		}
		self.connection.cursor.execute("""CALL Test.create_dungeon('{}','{}')"""
									   .format(dungeon_obj['difficulty_level']
											   , dungeon_obj['name']))
		self.connection.conn.commit()
		return self.get_dungeon(dungeon_obj['name'])


if __name__ == '__main__':
	dungeon = Dungeon()
	dungeon.create_dungeon(3)