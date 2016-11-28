from Connection import Connection
import json
from random import randint
from pprint import pprint

class Building():



	def __init__(self):
		pass

	def load_npcs(self, build_id):
		typ = self.connection.cursor.execute("""
			SELECT Type FROM Test.Building
			WHERE Test.Building. == %s 
			""", loc_id)

if __name__ == '__main__':
	building = Building()