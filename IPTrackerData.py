import os
import sqlite3

class IPTrackerData(object):
	sqlite_file = 'data.sqlite' 
	table_subnets = 'subnets'
	
	def __init__(self):		
		
		self.subnets = []
		self.conn = self.db_check()
		
		self.get_subnets()
		
		
		#self.db_close(conn)
		
	def db_check(self):
		try:
			if os.path.isfile('data.sqlite'):
				conn = sqlite3.connect(self.sqlite_file)
				return conn
			else:
				conn = sqlite3.connect(self.sqlite_file)
				self.db_create(conn)
				return conn
		except Error as e:
			print(e)
		return None
			
			
	def db_create(self, conn):
		print("Creating database ", self.sqlite_file)
		sql_subnets_table = """ CREATE TABLE IF NOT EXISTS subnets (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        IP text,
										mask text
                                    ); """
		#conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()

		c.execute(sql_subnets_table)

		
	def create_subnet(self, data):
		sql = ''' INSERT INTO subnets(name,IP,mask)
              VALUES(?,?,?) '''
		cur = self.conn.cursor()
		cur.execute(sql, data)
		self.conn.commit()
		return cur.lastrowid
	
	def get_subnets(self):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM subnets")
 
		rows = cur.fetchall()
		
		for row in rows:
			self.subnets.append(row[1])
		
	def db_close(self):
		self.conn.close()

		