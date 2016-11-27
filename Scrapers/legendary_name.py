import requests
import json
from pprint import pprint


link = 'https://donjon.bin.sh/fantasy/random/rpc.cgi?type=Legendary+Weapon&n=10'

loot_name = requests.get(link)
_loot = []
print(type(_loot))
for i in range(0,50):
	for loot in loot_name.json():
		_loot_name =  loot.split(',')[0]
		loot_description = ''.join(loot[0:])
		item = {
			'name':_loot_name,
			'loot_description':loot_description
		}
		_loot.append(item)


with open('loot.json', 'w') as file:
	json.dump(_loot, file)
	