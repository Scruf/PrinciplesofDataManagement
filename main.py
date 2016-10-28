from pprint import pprint
from Connection import Connection
from Character import Character
from Dungeon import Dungeon
from Monster import Monster
import sys

connection = Connection()

#Choice between character creation or character selection for loading
print("\n\n=============================="
	  "\nWelcome to the Dungeon Nights!\n"
	  "==============================\n\n"
	  "Please select one of the options to continue\n"
	  "1. Create New Character\n"
	  "2. Continue Game (UNDER DEVELOPMENT)")

#Instance of Character class
characterInst = Character()
option = input("Select: ")
if option == "1":
	character_name = input("Please enter name of the character (30 character limit): ")
	characterInst.create_character(character_name)
	print("Created " + character_name + "!")
elif option == "2":
	print("Under development...\n")
	characters  = characterInst.fetch_characters()
	for character in characters:
		print(character)
else:
	print("If you can't follow directions, this game isn't for you."
		  "\n\n=================================="
		  "\nThanks for playing Dungeon Nights!"
		  "\n==================================")
	sys.exit(0)

#Create dungeon method
def createDungeon(level):
	dungeonInst.create_dungeon(level)

	print("\nDungeons in DB (updated):")
	dungeons = dungeonInst.get_dungeons()
	for dungeon in dungeons:
		print(dungeon)

	showMonsters = input("\nShow monsters that could spawn in created dungeon? (Y/N): ")
	if showMonsters == "Y" or showMonsters == "y":

		#Instance of Monster class
		monsterInst = Monster()
		print("\nMonsters that may spawn in this dungeon:")
		pprint(monsterInst.fetch_monsters(level))

	print("\n=================================="
		  "\nThanks for playing Dungeon Nights!"
		  "\n==================================")



#Demos dungeon creation options
print("\nDemo of backend functionality\n"
	  "1. See current dungeons in system\n"
	  "2. Create a new dungeon\n")

#Instance of Dungeon class
dungeonInst = Dungeon()
dungOpt = input("Select: ")
if dungOpt == "1":
	print("\nDungeons in DB:")
	dungeons = dungeonInst.get_dungeons()
	for dungeon in dungeons:
		print(dungeon)

	createOpt = input("\nWould you like to create a new dungeon? (Y/N): ")
	if createOpt == "Y" or createOpt == "y":
		dungLvl = input("Enter dungeon level (1-5): ")
		createDungeon(dungLvl)
	else:
		print("\n=================================="
		  "\nThanks for playing Dungeon Nights!"
		  "\n==================================")
else:
	dungLvl = input("Enter dungeon level (1-5): ")
	createDungeon(dungLvl)
