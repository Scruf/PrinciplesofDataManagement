from Connection import Connection
import Combat
from random import randint


class Monster:
    def __init__(self):
        self.connection = Connection()

    #fetches all monsters currently in DB, returns dictionary
    def fetch_monsters(self, dungeon_level):
        self.connection.cursor.execute("""CALL Test.fetch_monsters('{}')""".format(dungeon_level))
        self.connection.conn.commit()

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchall():
            dictionary = dict(zip(key_list,list(data)))
            results.append(dictionary)

        return results

    def get_monst_attrs(self, monst_id):
        self.connection.cursor.execute("""SELECT challenge_level, hitpoints, damage, defense FROM Test.Monster
                                                    WHERE Test.Monster.monster_id =%s """, monst_id)
        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        return dict(zip(key_list, list(self.connection.cursor.fetchall()[0])))

    def spawn_monster(self, player_id, quest_id, challenge_level, loc_id):
        num = randint(1, 17)
        self.connection.cursor.execute("""SELECT * FROM Test.Monster
                                             WHERE monster_id = {}"""
                                             .format(num) )


        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        monster = dict(zip(key_list,list(self.connection.cursor.fetchall()[0])))

        print("You've encountered a {}!".format(monster['monster_name']))
        combatInst = Combat.Combat()
        combatInst.initiate_combat(player_id, monster['monster_id'], loc_id, quest_id)



