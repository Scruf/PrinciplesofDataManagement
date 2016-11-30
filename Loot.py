from Connection import Connection
from random import randint, choice, uniform
import json


class Loot:
    def __init__(self):
        self.connection = Connection()

    '''fetches all loot of a certain rarity and type'''
    def fetch_loot(self, loot_rarity, loot_type):
        self.connection.cursor.execute("""CALL Test.fetch_loot('{}', '{}')""".format(loot_rarity, loot_type))
        self.connection.conn.commit()

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchall():
            dictionary = dict(zip(key_list,list(data)))
            results.append(dictionary)

        return results

    def get_loot_item(self, loot_id):
        self.connection.cursor.execute("""SELECT * FROM Loot 
                                            WHERE loot_id='{}'""".format(loot_id))

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchall():
            dictionary = dict(zip(key_list,list(data)))
            results.append(dictionary)

        return results[0]

    '''Randomly selects the rarity level of loot'''
    @staticmethod
    def get_drop_rarity():
        rarity_roll = randint(0,100)
        rarity_str = ""

        if rarity_roll <= 60:
            rarity_str = "Common"
        elif rarity_roll > 60 & rarity_roll <= 80:
            rarity_str = "Uncommon"
        elif rarity_roll > 80 & rarity_roll <= 94:
            rarity_str = "Rare"
        elif rarity_roll >= 95:
            rarity_str = "Legendary"

        return rarity_str

    '''Randomly selects reward based on rarity and type'''
    @staticmethod
    def determine_reward_amount(loot_rarity, loot_type):
        reward_amnt = 1

        if loot_type == "Currency":
            if loot_rarity == "Common":
                reward_amnt = randint(10,30)
            elif loot_rarity == "Uncommon":
                reward_amnt = randint(50,80)
            elif loot_rarity == "Rare":
                reward_amnt = randint(100,130)
            else:
                reward_amnt = randint(150,225)
        elif loot_rarity == "Common":
            if loot_type == "Battle Item":
                reward_amnt = 3

        return reward_amnt

    '''Adds quantity of loot_id to Character_loot'''
    def add_to_inventory(self, player_id, loot_id, quantity):
        self.connection.cursor.execute(
            """CALL Test.add_to_inventory('{}', '{}', '{}')""".format(player_id, loot_id, quantity))
        self.connection.conn.commit()

    '''Removes items from Character_loot for player_id'''
    def remove_from_inventory(self, player_id, loot_id, quantity):
        self.connection.cursor.execute(
            """CALL Test.remove_from_inventory('{}', '{}', '{}')""".format(player_id, loot_id, quantity))
        self.connection.conn.commit()

    '''Equips item for character. Adjusts attack/defense accordingly'''
    def equip_item(self, player_id, loot_id, loot_type):
        self.connection.cursor.execute(
            """CALL Test.equip_item('{}', '{}', '{}')""".format(player_id, loot_id, loot_type))
        self.connection.conn.commit()

    '''Unequips item for character. Adjusts attack/defense accordingly'''
    def unequip_item(self, player_id, loot_id, loot_type):
        self.connection.cursor.execute(
            """CALL Test.unequip_item('{}', '{}', '{}')""".format(player_id, loot_id, loot_type))
        self.connection.conn.commit()

    '''Get equipped items'''
    def get_equipped_items(self, player_id):
        self.connection.cursor.execute(
            """CALL Test.get_equipped_items('{}')""".format(player_id))

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchall():
            dictionary = dict(zip(key_list, list(data)))
            results.append(dictionary)

        return results


    '''Creates a legendary weapon'''
    def create_legendary_weapon(self, loot_name, loot_atk_mod, loot_val, loot_desc):
        self.connection.cursor.execute(
            """CALL Test.create_legendary_weapon('{}', '{}', '{}', '{}')""".format(loot_name, loot_atk_mod, loot_val, loot_desc))
        self.connection.conn.commit()

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchone():
            dictionary = dict(zip(key_list, list(data)))
            results.append(dictionary)
        item_result = results[0]
        item_id = item_result["loot_id"]

        return item_id

    '''Determines reward for quests and monster drops. If dropped by monster, instantly added to inventory'''
    def determine_reward(self, player_id, reward_context):
        reward_type = ""
        type_roll = randint(0,100)
        reward_rarity = Loot.get_drop_rarity()

        if reward_rarity == "Legendary":
            legendary = []
            with open('loot.json') as data:
                legendary = json.load(data)

            legendary_item = legendary[randint(0,len(legendary))]
            loot_name = legendary_item["name"]
            loot_desc = legendary_item["loot_description"]

            atk_mod_raw = uniform(0.6, 1.3)
            atk_mod = ("%.2f" % round(atk_mod_raw, 2))

            loot_val = randint(200, 375)
            loot_id = Loot.create_legendary_weapon(self, loot_name, atk_mod, loot_val, loot_desc)

            reward = dict(loot_id=1)

            return reward

        elif reward_context == "Monster drop":
            if type_roll <= 33:
                reward_type = "Currency"
            elif 33 < type_roll <= 66:
                reward_type = "Battle Item"
            elif 66 < type_roll <= 85:
                reward_type = "Armor"
            else:
                reward_type = "Weapon"
        elif reward_context == "Rescue Quest" or reward_context == "Kill Quest":
            if type_roll <= 50:
                reward_type = "Currency"
            elif 50 < type_roll <= 70:
                reward_type = "Battle Item"
            elif 70 < type_roll <= 85:
                reward_type = "Armor"
            else:
                reward_type = "Weapon"
        elif reward_context == "Fetch Quest":
            if type_roll <= 75:
                reward_type = "Currency"
            elif 75 < type_roll <= 90:
                reward_type = "Battle Item"
            elif 90 < type_roll <= 95:
                reward_type = "Armor"
            else:
                reward_type = "Weapon"

        reward_amt = Loot.determine_reward_amount(reward_rarity, reward_type)
        all_possible_loot = Loot.fetch_loot(self, reward_rarity, reward_type)

        random_loot_id = choice(all_possible_loot)["loot_id"]

        reward = {"{}".format(random_loot_id): reward_amt}

        #Add reward to inventory if this is from a monster encounter
        if reward_context == "Monster drop":
            Loot.add_to_inventory(self, player_id, random_loot_id, reward_amt)

        return reward
