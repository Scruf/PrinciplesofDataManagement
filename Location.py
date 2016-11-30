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

	def get_location_id(self, loc_name):
		self.connection.cursor.execute("""
			SELECT location_id FROM Test.Location
			WHERE Test.Location.location_name='{}'"""
			.format(loc_name))

		return self.connection.cursor.fetchone()[0]


	def populate(self, loc_id):
		random_buildings = random.sample(range(1,9),self.get_num_buildings(loc_id))
		for building in random_buildings:

			self.connection.cursor.execute("""
				CALL Test.populate_location('{}', '{}')
				""".format(building, loc_id))

			self.connection.conn.commit()
	"""
		@method get_current_location will retriece current location of the player
				@param character_name is a name of the character for whom curent location
										will be retrieced 
	"""
	def get_current_location(self,character_name):
		self.connection.cursor.execute("""SELECT curr_location_id
										  FROM Test.Character
										  WHERE character_name = '{}'""".format(character_name)
		)
		self.connection.conn.commit()
		location_id =  self.connection.cursor.fetchone()[0]
		return int(location_id)

	"""
		@method random_town_name() will return random town name
	"""
	def random_town_name(self):
		town_names = []
		with open('city.json') as data:
			town_names = json.load(data)
		return town_names[randint(0,len(town_names)-1)]['name']

	"""
		@method get_player_id(character_name) will return the player id
			@param character_name  will return the player id
	"""
	def get_player_id(self,character_name):
		characrer_query = """	SELECT player_id
								 FROM Test.Character
								 WHERE character_name = '{}'""".format(
								 	character_name
			)
		self.connection.cursor.execute(characrer_query)
		self.connection.conn.commit()
		return self.connection.cursor.fetchone()[0]

	"""
		@method get_location(character_name) will drop player to a new location
				@param character_name is characte_name is character name which will
					be droped in the game
	"""
	def get_player_name(self,player_id):
		player_name_query = """SELECT character_name
							   FROM Test.Character
							   WHERE player_id  = '{}'""".format(
							   player_id
		)
		self.connection.cursor.execute(player_name_query)
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
				'location_name':str(self.random_town_name()).capitalize(),
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
				# 'town_description':welcome_str,
				'town_description': results[0]['location_type'],
				'player_name':character_name,
				'buildings':buildings,
				'city_name':results[0]['location_name']
			}

			return town_obj

	# new towns get_new_towns will generate new locations
	def get_new_towns(self, character_name):
		#get player id
		player_id = self.get_player_id(character_name)
		#get visited towns
		visited_town_query = """SELECT location_name
						   		FROM Test.Location
						   		WHERE character_id = '{}'""".format(
						   		player_id
							)
		#execute town_query
		self.connection.cursor.execute(visited_town_query)
		self.connection.conn.commit()
		#fetch visited city if any
		visited = []

		for city in self.connection.cursor.fetchall():
			visited.append(city[0])
		town_types  = ['Town','City','Village','Hamlet']
		new_towns = []

		for i in range(0,4):
			town_obj = {
				"city_name":str(self.random_town_name()).capitalize(),
				"city_type":town_types[randint(0,len(town_types)-1)],
				"discovered_from_id":self.get_current_location(character_name)
			}

			new_towns.append(town_obj)
			#new town query string
			new_town_query = """INSERT INTO Test.Location(location_name,
														  location_type,
														  discovered_from_id,
														  location_limit,
														  character_id) VALUES(
									'{}','{}','{}','{}','{}'
								)""".format(
										town_obj['city_name'],town_obj['city_type'],
										town_obj['discovered_from_id'],randint(2,8),
										self.get_player_id(character_name)
								)
			self.connection.cursor.execute(new_town_query)
			self.connection.conn.commit()

		return new_towns

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

	"""
		@method def go_to(location_name,player_id) will move player to the location of the player
				@param location_name is the location name where player wants to go
				@param player_id is the id of the player  
					
	"""

	def go_to(self,location_name,player_id):
		#create location query to retriece location id
		location_id_query =  """SELECT location_id 
								FROM Test.Location
								WHERE location_name = '{}'
								AND character_id = '{}'""".format(
									location_name,player_id
								)
		#execute the location query
		self.connection.cursor.execute(location_id_query)
		self.connection.conn.commit()
		#retrieve location id from the query
		location_id = self.connection.cursor.fetchone()[0]
		#update location query
		update_location = """CALL Test.update_location('{}','{}')""".format(
			location_id,player_id
		)
		self.connection.cursor.execute(update_location)
		self.connection.conn.commit()
		player_name_query = """SELECT character_name
						 FROM Test.Character
						 WHERE player_id = '{}'""".format(
						 	player_id
						 )

		self.connection.cursor.execute(player_name_query)
		self.connection.conn.commit()
		
		character_name = self.connection.cursor.fetchone()[0]
		#populate town
		self.populate(location_id)
		#return that city description
		return self.get_location(character_name)
	"""
	@method def leave(player_id,back) will allow player to move back and forth
				@param back will determine wheter player wants to move back or forward

	"""
	def leave(self,player_id,back):
		#if false than we are moving forward and the player
		#will get new towns to go to 
		if not back:
			#first lets get current_loc
			cur_loc = self.get_current_location(self.get_player_name(player_id))

			#check whether this city has any discoveries 
			#if not than call new cities
			#otherwise display old city which were discovered from that city
			discovered_query = """SELECT *
								  FROM Test.Location
								  WHERE discovered_from_id = '{}'""".format(
								  	cur_loc
								  )
			self.connection.cursor.execute(discovered_query)
			
			self.connection.conn.commit()
			
			discovered_cities = []

			for city in self.connection.cursor.fetchall():
				city_obj = {
					'city_name':city[1],
					'city_type':city[3],
					'discovered_from_id':city[4]
				}
				discovered_cities.append(city_obj)
			#if the length is greater than 0 than it means we found some city previously discovered
			if len(discovered_cities)>0:
				return discovered_cities
			else:
				return self.get_new_towns(self.get_player_name(player_id))

			#now lets find the cities were player was
			# return self.get_new_towns(self.get_player_name(player_id))

		else:
			#We are moving backwards
			prev_location = self.get_current_location(self.get_player_name(player_id))
			#get back to the city 
			#get discovered from
			discovered_from_query ="""SELECT discovered_from_id
								  	  FROM Test.Location
								  	  WHERE location_id = '{}'""".format(prev_location)
			self.connection.cursor.execute(discovered_from_query)
			self.connection.conn.commit()
			discovered_from_id = self.connection.cursor.fetchone()[0]

			#update current location of the player to a previous location
			go_back_query  = """CALL Test.update_location('{}','{}')""".format(
				discovered_from_id,player_id
			)
			# print(go_back_query)
			#execute update_location
			self.connection.cursor.execute(go_back_query)
			self.connection.conn.commit()
			#return previous locatio 
			return self.get_location(self.get_player_name(player_id))

			
	def map(self,player_id):
		# current_id = self.get_current_location(self.get_player_name(player_id))
		map_query = """SELECT location_id, location_name, location_type
					   FROM Test.Location
					   WHERE character_id = '{}'""".format(player_id)

		self.connection.cursor.execute(map_query)
		self.connection.conn.commit()
		discovered_locations = []
		for city in self.connection.cursor.fetchall():
			city ={
				'city_id':city[0],
				'city_name':city[1],
				'city_type':city[2]
			}
			discovered_locations.append(city)
			
		return discovered_locations


if __name__ == '__main__':
	location = Location()
	print(location.map('11'))
	
