from Connection import Connection
from Character import Character
from Monster import Monster
from random import randint
from tabulate import tabulate


class Combat:
    def __init__(self):
        self.connection = Connection()

    def initiate_combat(self, player_id, monster_id):
        
        preCombatCharacter = Character()
        preCombatCharAttrs = preCombatCharacter.get_currplayer_attr(player_id)
        preCombatMonster = Monster()
        preCombatMonsterAttrs = preCombatMonster.get_monst_attrs(monster_id)
        monstHealth = preCombatMonsterAttrs['hitpoints']
        print("\nYou have entered combat!\n")
        while (monstHealth > 0):
            characterInst = Character()
            monstInst = Monster()
            charAttrs = {}
            monstAttrs = {}
            loot = {}
            charAttrs = characterInst.get_currplayer_attr(player_id)
            monstAttrs = monstInst.get_monst_attrs(monster_id)
            print("\nMonst Hit Points: {}\n".format(monstAttrs['hitpoints']))
            
            print (
                "1. Attack\n"
                "2. Defend\n"
                "3. Use Item\n")
            choice = input ("Select: ")
            if choice == "1":
                #attack
                hitChance = randint(0, 10)
                #decide if player attacks or misses
                if (charAttrs['character_level'] < 5):
                    if (hitChance > 3):
                        hit = True
                    else:
                        hit = False
                else:
                    if (hitChance > 2):
                        hit = True
                    else:
                        hit = False

                #do a level comparison to decide a modifier
                diff = charAttrs['curr_attack'] - monstAttrs['defense']
                if (diff > 3):
                    #level check
                    levelDiff = charAttrs['character_level'] - monstAttrs['challenge_level']
                    if (levelDiff == 0):
                        mult = 1
                    elif (levelDiff < 0):
                        mult = .75
                    elif (levelDiff > 0):
                        mult = 1.25
                    totalDamage = charAttrs['curr_attack'] * mult
                else:
                    totalDamage = randint(1, 4)

                #There's a hit
                if hit == True:
                    print("\nThat's a hit for {} damage!\n".format(totalDamage))
                    oldHitP = monstAttrs['hitpoints']

                    if (oldHitP - totalDamage) < 0:
                        newHitP = 0
                    else:
                        newHitP = oldHitP - totalDamage

                    print("\nThe monster is down to {} hitpoints!\n".format(newHitP))

                    if newHitP == 0:
                        print("\nYou've killed the monster!\n")

                    monstHealth = newHitP
                    self.connection.cursor.execute("""UPDATE Monster
                                                    SET hitpoints={}
                                                    WHERE monster_id={}""".format(newHitP, monster_id))
                    self.connection.conn.commit()
                else:
                    print("\nYou've missed!\n")

            elif choice == "2":
                #defend
                pass
            elif choice == "3":
                loot = {}
                loot = characterInst.get_currplayer_loot(player_id)
                print("Select Battle Item From Inventory: \n")
                i = 0
                table = []
                
                for item in loot:
                    table.append([item['loot_name'],
                                    item['health_modifier'],
                                    item['defense_modifier'],
                                    item['attack_modifier'],
                                    item['quantity']])

                print (tabulate(table, headers=['Name', 
                    'Health Modifier', 
                    'Defense Modifier', 
                    'Attack Modifier', 
                    'Quantity'], showindex='always'))

                choice = input ("Select: ")
                choiceInt = int(choice)
                itemChoice = loot[choiceInt]
                print("\nYou chose: {}\n".format(itemChoice['loot_name']))
                #defense modifier
                if (itemChoice['defense_modifier'] > 0):
                    increment = charAttrs['base_defense'] * itemChoice['defense_modifier']
                    curr_def = charAttrs['curr_defense'] + increment
                    self.connection.cursor.execute(
                        """UPDATE Test.Character SET curr_defense='{}' WHERE player_id ='{}'""".format(
                                curr_def, player_id))
                    self.connection.conn.commit()
                    print("Defense increased by {}!".format(increment))
                    print("Defense now at {}".format(curr_def))
                #health modifier
                elif (itemChoice['health_modifier'] > 0):
                    increment = charAttrs['max_hp'] * itemChoice['health_modifier']
                    if (charAttrs['curr_hp'] + increment) >= charAttrs['max_hp']:
                        curr_health = charAttrs['max_hp']
                    else:
                        curr_health = charAttrs['curr_hp'] + increment
                    print("Health increased by {}!\n".format(increment))
                    print("Health now at {}\n".format(curr_health))
                #attack modifier
                elif (itemChoice['attack_modifier'] > 0):
                    increment = charAttrs['base_attack'] * itemChoice['attack_modifier']
                    curr_health = charAttrs['curr_attack'] + increment
                    print("Attack increased by {}!".format(increment))
