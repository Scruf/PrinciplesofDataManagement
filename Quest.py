from Connection import Connection
from Monster import Monster
import json
from random import randint
from pprint import pprint

class Quest():



	def __init__(self):
		self.connection = Connection()

	def initiate_quest(self, quest_id, player_id, loc_id):
		#get quest
		monsterInst = Monster()
		self.connection.cursor.execute("""SELECT * FROM Quest WHERE quest_id = {}""".format(quest_id))

		results = self.connection.cursor.fetchall()
		key_list = []
		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		quest = dict(zip(key_list, list(results[0])))

		#get dungeon
		self.connection.cursor.execute("""SELECT * FROM Dungeon WHERE id={}""".format(quest['dungeon_id']))
		results = self.connection.cursor.fetchall()
		key_list = []

		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		dungeon = dict(zip(key_list, list(results[0])))

		print("\nNow entering {}...\n".format(dungeon['dungeon_name']))
		monsterInst.spawn_monster(player_id, quest_id, dungeon['difficulty_level'], loc_id)

	def get_quest_type(self, quest_id):
		self.connection.cursor.execute("""SELECT type FROM Quest WHERE quest_id={}""".format(quest_id))
		return self.connection.cursor.fetchall()[0][0]

	def finish_quest(self, quest_id, player_id):
		self.connection.cursor.execute("""UPDATE Quest_log SET finished=true WHERE quest_id={} AND character_id={}""".format(quest_id, player_id))
		self.connection.conn.commit()




if __name__ == '__main__':
	quest = Quest()