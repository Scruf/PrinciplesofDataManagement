# Dungeon Nights

## Install instructions
In order to run the program, first you'll need to install python modules PyMySQL and Tabulate
* To install PyMySQL, run “pip3 install pymysql”
* To install Tabulate, run “pip3 install tabulate”

## Run instructions
In order to play Dungeon Nights:
* To start, run "python3 main.py" from inside the project directory
* After started, instructions for what to do will be displayed. Follow them and enjoy!

## Features
Like many game developers are quick to learn, our initial plan was far too vast for our given timeline.
While we would have loved to include all the features we fantasized, our deadline limited what we were able to accomplish

### Gameplay features (involving DB calls)
* Character creation/loading
* Travel to/Leave location
* Enter building
* Talk to NPC
* Accept quest
* Fight monster
* Display character map/inventory/questlog

### Theoretical features (of existing implementations of DB calls)
These are features that would in theory work if they were connected by other working Python functions
Ex: You can equip/unequip weapons/armor, which modifies multiple tables based on queried values,
but since combat and quests don't give you items due to gameflow problems, you never get a chance to equip

* Equipping/unequipping weapons/armor
** This can be tested though if you load as the character 'Zachary', who does have items
* Getting loot from quest completion/monster drop
* Completing quest by returning to NPC
* Buying/Selling items to NPCs 