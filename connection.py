import pymysql
from pprint import pprint
conn = pymysql.connect(host='66.175.208.103',\
						  port = 3306, user='root',\
						  passwd='nT2K64bwHB!UR+4JR%P%S?5rYMcZJkw&',
						  db='Test')
cursor = conn.cursor()
cursor.execute("""CALL Test.create_character('{}')""".format("BOb") )
conn.commit()
