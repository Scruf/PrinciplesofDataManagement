from Connection import Connection


class Character():

	def __init__(self):
		self.connection = Connection()



	def create_character(self,character_name):
		self.connection.cursor.execute("""CALL Test.create_character('{}')"""
										.format(character_name))
		self.connection.conn.commit()


