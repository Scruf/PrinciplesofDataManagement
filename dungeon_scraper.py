import json
from Connection import Connection

with open('data.json') as data:
	temp = json.load(data)

print(temp)