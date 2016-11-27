from Connection import Connection


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
