from Connection import Connection
class Character():


	def __init__(self):
		self.connection = Connection() 





	def get_name(self):
		return self.name

	def create_character(self,name):
		self.name = name
		self.connection.cursor.execute("""CALL Test.create_character('{}')""".format(name))
		self.connection.conn.commit()
