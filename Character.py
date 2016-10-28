from Connection import Connection


class Character():

	def __init__(self):
		self.connection = Connection()

	#creates a character in DB
	def create_character(self,character_name):
		self.connection.cursor.execute("""CALL Test.create_character('{}')"""
										.format(character_name))
		self.connection.conn.commit()

	#fetches all characters currently in DB
	def fetch_characters(self):
		self.connection.cursor.execute("""SELECT character_name FROM Test.Character""")
		self.connection.conn.commit()

		results = []
		for data in self.connection.cursor.fetchall():
			results.append(data)

		return results