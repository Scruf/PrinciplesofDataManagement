from Connection import Connection
from random import randint
from pprint import pprint 
import random
import json

class Location():

	def __init__(self):
		self.connection = Connection()

	def get_num_buildings(self, loc_id):
		self.connection.cursor.execute("""
			SELECT location_limit FROM Test.Location
			WHERE Test.Location.location_id = %s 
			""", loc_id)

		self.connection.conn.commit()

		return self.connection.cursor.fetchone()[0]


	def populate(self, loc_id):
		random_buildings = random.sample(range(1,9),self.get_num_buildings(loc_id))
		for building in random_buildings:

			self.connection.cursor.execute("""
				CALL Test.populate_location('{}', '{}')
				""".format(building, loc_id))

			self.connection.conn.commit()

	
	
	def random_town_name(self):
		town_names = []
		with open('city.json') as data:
			town_names = json.load(data)
		return town_names[randint(0,len(town_names)-1)]['name']


	def get_player_id(self,character_name):
		characrer_query = """SELECT player_id
								 FROM Test.Character
								 WHERE character_name = '{}'""".format(
								 	character_name
			)
		self.connection.cursor.execute(characrer_query)
		self.connection.conn.commit()
		return self.connection.cursor.fetchone()[0]


	def get_location(self,character_name):
		#Execute the query

		self.connection.cursor.execute("""SELECT curr_location_id 
										  FROM Test.Character
										  WHERE character_name = '{}'""".format(character_name))

		cur_location = int(self.connection.cursor.fetchone()[0])
		#if its a new game than populate the town 
		if cur_location == -1:
			town_types  = ['Town','City','Village','Hamlet']

			
			character_id = self.get_player_id(character_name)
			new_town = {
				'location_type':town_types[randint(0,len(town_types)-1)],
				'location_name':self.random_town_name(),
				'location_limit':randint(2,8),
				'discovered_from':-1,
				'character_id':character_id
			}

			add_to_town_query = """CALL Test.add_location('{}','{}','{}','{}','{}')""".format(
						new_town['location_name'],new_town['location_limit'],new_town['location_type'],
						'-1',new_town['character_id']
			)

			self.connection.cursor.execute(add_to_town_query)
			self.connection.conn.commit()

			location_id = """SELECT location_id
							 FROM Test.Location
							 WHERE location_name = '{}'
							 	AND  location_limit = '{}'
							 	AND location_type = '{}'
							 	AND character_id = '{}'
							 """.format(
				new_town['location_name'],new_town['location_limit'],new_town['location_type'],
				new_town['character_id']
			)
			self.connection.cursor.execute(location_id)
			self.connection.conn.commit()
			_id =  self.connection.cursor.fetchone()[0]
			self.populate(_id)
			update_query = """CALL Test.update_location('{}','{}')""".format(
					_id,new_town['character_id']
			)
			self.connection.cursor.execute(update_query)
			self.connection.conn.commit()

			return self.get_location(character_name)

		#do not populate the town
		else:


			buildings =  self.get_building_names(cur_location)
			#retrieve the cur_location

			#Dictionry which will hold city description
			self.connection.cursor.execute(
				"""CALL Test.location_description ('{}')""".format(
					cur_location)
			)
			self.connection.conn.commit()
			
			key_list = []

			for description in self.connection.cursor.description:
				key_list.append(description[0])

			results  = [] 

			for data in self.connection.cursor.fetchall():
				dictionary = dict(zip(key_list,list(data)))
				results.append(dictionary)

			welcome_str = "Welcome %s to the %s of %s\n you see "%(character_name,results[0]['location_type'],
																	results[0]['location_name'])

			for building in buildings:
				welcome_str  = welcome_str + ' a ' + building + ','

			welcome_str = welcome_str  + ' near you.' 

			town_obj = {
				'town_description':welcome_str,
				'player_name':character_name,
				'buildings':buildings,
				'city_name':results[0]['location_name']
			}

			return town_obj


	#get_building_names will retrieve all building name based on the location_id
	def get_building_names(self,location_id):
		query  = """SELECT building_id
					FROM Test.Location_buildings
					WHERE Test.Location_buildings.location_id = '{}'""".format(
						location_id
					)
		self.connection.cursor.execute(query)
		self.connection.conn.commit()
		building_name = []
		for building_id in self.connection.cursor.fetchall():
			building_name_query = """SELECT Type
									 FROM Test.Buildings
									 WHERE building_id = '{}'""".format(building_id[0])

			self.connection.cursor.execute(building_name_query)
			self.connection.conn.commit()
			building_name.append(self.connection.cursor.fetchone()[0])

		return building_name





if __name__ == '__main__':
	location = Location()
	print(location.get_location('Shalimar'))
	
