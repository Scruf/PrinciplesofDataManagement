from pprint import pprint
from Connection import Connection
from Character import Character
from Dungeon import Dungeon
from Monster import Monster
import sys

connection = Connection()

# Choice between character creation or character selection for loading
'''
# Beginning of actual game, not part of the demo.
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
'''


# Create dungeon method
def createDungeon(level):
    dungeon = dungeonInst.create_dungeon(level)

    print("\nDungeons created:")
    print("\tname: {}\n\tdifficulty: {}\n".format(dungeon["dungeon_name"], dungeon["difficulty_level"]))

    showMonsters = input("\nShow monsters that could spawn in created dungeon? (Y/N): ")
    if showMonsters[0].lower() == 'y':
        # Instance of Monster class
        monsterInst = Monster()
        print("\nMonsters that may spawn in this dungeon:")
        for monster in monsterInst.fetch_monsters(level):
            print("\tname: {}\n\thitpoints: {}\n\tdamage: {}\n\tdefense: {}\n\tattack type: {}\n\tchallenge level: {}\n\t"
                  "max loot dropped: {}\n".format(monster['monster_name'], monster['hitpoints'], monster['damage'],
                                                monster['defense'], monster['attack_type'], monster['challenge_level'],
                                                monster['max_loot']))
        #pprint(monsterInst.fetch_monsters(level))


# Demos dungeon creation options
while True:
    print("\nDemo of backend functionality\n"
          "1. See players in the system currently\n"
          "2. Create a new player.\n"
          "3. See current dungeons in system\n"
          "4. Create a new dungeon\n"
          "5. Quit\n")

    # Instance of Dungeon class
    dungeonInst = Dungeon()
    choice = input("Select: ")
    characterInst = Character()
    if choice == "1":
        characters = characterInst.fetch_characters()
        print("Characters in system:")
        for character in characters:
            print("\t"+character)
    elif choice == "2":
        character_name = input("Please enter name of the character (30 character limit): ")
        characterInst.create_character(character_name)
        print("Created " + character_name + "!")
    elif choice == "3":
        print("\nDungeons in DB:")
        dungeons = dungeonInst.get_dungeons()
        for dungeon in dungeons:
            print("\tname: {}\n\tdifficulty: {}\n".format(dungeon["dungeon_name"],dungeon["difficulty_level"]))
    elif choice == "4":
        dungLvl = input("Enter dungeon level (1-5): ")
        createDungeon(dungLvl)
    elif choice == "5":
        print("===================================\n"
              "Thanks for testing out our backend!\n"
              "===================================")
        quit()
