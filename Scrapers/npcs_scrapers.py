import requests
import json
from pprint import pprint
import time

link =  'http://npcgenerator.azurewebsites.net/_/npc'

npc_list =  []
for i in range(0,1000):
	npcs_request = requests.get(link).json()
	npc_list.append({'description':npcs_request['description'],
					 'hook':npcs_request['hook']['description'],
					 'physical':npcs_request['physical'],
					 'traits':[npcs_request['pquirks']['description'],npcs_request['ptraits']['traits1'],
					 			npcs_request['ptraits']['traits1']]
				    })
	pprint(npc_list[i])

	time.sleep(3)


with open('npc.json', 'w') as file:
	json.dump(npc_list, file)