from Connection import Connection
from random import randint, choice


class Loot:
    def __init__(self):
        self.connection = Connection()

    #fetches all loot of a certain rarity and type
    def fetch_loot(self, loot_rarity, loot_type):
        self.connection.cursor.execute("""CALL Test.fetch_loot('{}')""".format(loot_rarity, loot_type))
        self.connection.conn.commit()

        key_list = []
        for description in self.connection.cursor.description:
            key_list.append(str(description[0]))

        results = []
        for data in self.connection.cursor.fetchall():
            dictionary = dict(zip(key_list,list(data)))
            results.append(dictionary)

        return results

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

    def determine_reward(self, reward_context):
        reward_type = ""
        type_roll = randint(0,100)
        reward_rarity = Loot.get_drop_rarity()
        if reward_context  == "Legendary":
            legendary  = []
            with open('loot.json') as data:
                legendary = json.load(data)

            legendary_item = legendary[randint(0,len(legendary))]
            

        if reward_context == "Monster drop":
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
        random_loot = choice(all_possible_loot)

        reward = dict({random_loot: reward_amt})

        #add to inventory
        return reward
