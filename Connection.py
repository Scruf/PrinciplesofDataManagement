import pymysql


class Connection():


	def __init__(self):
		self.conn = pymysql.connect(host='66.175.208.103',\
						  port = 3306, user='root',\
						  passwd='nT2K64bwHB!UR+4JR%P%S?5rYMcZJkw&',
						  db='Test')
		self.cursor = self.conn.cursor()