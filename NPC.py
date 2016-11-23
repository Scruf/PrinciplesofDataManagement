from Connection import Connection
import json
from random import randint
from pprint import pprint

class NPC():



	def __init__(self):
		pass

	"""
		@method get_npc will return a random npc from the npc.json
	"""
	def get_npc(self):
		npc_list = []
		
		with open('npc.json') as data:
			npc_list =  json.load(data)

		return npc_list[randint(0,len(npc_list))]







if __name__ == '__main__':
	npc =  NPC()
	pprint(npc.get_npc())
