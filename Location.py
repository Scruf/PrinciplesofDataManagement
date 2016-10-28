from Connection import Connection
from random import randint

class Location():

	def __init__(self):
		self.connection = Connection()

	def get_num_buildings(self, loc_id):
		num_buildings = self.connection.cursor.execute("""
			SELECT num_buildings FROM Test.Location
			WHERE Test.Location.Location_id == %s 
			""", loc_id)

	def populate(self, loc_id):
		for i in range(0, 2):
			random = randint(1, 3)
			self.connection.cursor.execute("""
				CALL Test.populate_location('{}', '{}')
				""".format(random, loc_id))
			self.connection.conn.commit()


if __name__ == '__main__':
	location = Location()