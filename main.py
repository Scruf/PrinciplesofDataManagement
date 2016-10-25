from pprint import pprint
from Connection import Connection
from Character import Character

connection = Connection()
character = Character()
print("Welcome to the Dungeon Knigts\n"\
	  "Please select one of the options to continue\n"\
	  "1. To Create a character\n"\
	  "2. Continue where you left off\n")

option = input("Selection: ")
if option == "1":
	character_name = input("Please enter name of the character: ")
	character.create_character(character_name)
else:
	print("Nope")