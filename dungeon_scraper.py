import json
from Connection import Connection
from pprint import pprint
from random import randint

with open('data.json') as data:
	dungen_names = json.load(data)

for dungen in dungen_names:
	pprint(dungen)

	