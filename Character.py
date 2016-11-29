from Connection import Connection


class Character():

	def __init__(self):
		self.connection = Connection()

	#creates a character in DB
	def create_character(self,character_name):
		self.connection.cursor.execute("""CALL Test.create_character('{}')"""
										.format(character_name))
		self.connection.conn.commit()

	def get_char_id(self, char_name):
		self.connection.cursor.execute("""SELECT player_id FROM Test.Character WHERE Test.Character.character_name = %s """, char_name)

		char_id = self.connection.cursor.fetchall()[0][0]
		return char_id

	#fetches character level by player_id
	def get_char_level(self, char_id):
		self.connection.cursor.execute("""SELECT character_level FROM Test.Character 
													WHERE Test.Character.player_id = %s """, char_id)
		level = self.connection.cursor.fetchall()[0][0]
		return level

	#gets player attributes needed for combat
	def get_currplayer_attr(self, char_id):
		self.connection.cursor.execute("""SELECT character_level, curr_attack, base_damage, curr_defense, base_defense, 
													max_hp, curr_hp, curr_xp FROM Test.Character
													WHERE Test.Character.player_id =%s """, char_id)
		key_list = []
		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		return dict(zip(key_list, list(self.connection.cursor.fetchall()[0])))

	#get player loot
	def get_currplayer_loot(self, char_id):
		self.connection.cursor.execute("""CALL Test.get_character_inventory_for_combat('{}')"""
									   .format(char_id))
		results = self.connection.cursor.fetchall()
		key_list = []
		for description in self.connection.cursor.description:
			key_list.append(str(description[0]))

		i = 0
		loot = []
		for item in results:
			entry = dict(zip(key_list, list(results[i])))
			loot.append(entry)
			i = i + 1

		return loot

	#fetches all characters currently in DB
	def fetch_characters(self):
		self.connection.cursor.execute("""SELECT character_name FROM Test.Character""")
		self.connection.conn.commit()

		results = []
		for data in self.connection.cursor.fetchall():
			results.append(data[0])

		return results