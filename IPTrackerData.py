import os
import sqlite3
import ipaddress
import csv
import datetime
from pathlib import Path

class IPTrackerData(object):
	CURRENT_DIR = os.path.dirname(__file__)
	USER_HOME_DIR = Path.home()
	USER_CONFIG_DIR = os.path.join(USER_HOME_DIR,'.config/IPTRACKER')
	sqlite_file = os.path.join(USER_CONFIG_DIR, 'data.sqlite')
	#sqlite_file = 'data.sqlite' 
	table_subnets = 'subnets'
	
	if not os.path.exists(USER_CONFIG_DIR):
		os.makedirs(USER_CONFIG_DIR)
	
	def __init__(self):		
		
		self.subnets = []
		self.conn = self.db_check()
		
		self.get_subnets()
		
		
		#self.db_close(conn)
		
	def db_check(self):
		try:
			if os.path.isfile(self.sqlite_file):
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
		
		#create IP table 
		sql_ips_table = """ CREATE TABLE IF NOT EXISTS ips (
                                        id integer PRIMARY KEY,
										subnetid integer,
                                        IP text NOT NULL,
										Status text,
                                        HostName text,
										Note text
                                    ); """
		#conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()

		c.execute(sql_ips_table)

		
	def create_subnet(self, data):
		sql = ''' INSERT INTO subnets(name,IP,mask)
              VALUES(?,?,?) '''
		cur = self.conn.cursor()
		cur.execute(sql, data)
		self.conn.commit()
		return cur.lastrowid
		
	def create_ips(self, data):
		_ip = ipaddress.ip_network(data[1]+"/"+data[2])

		#create network address entry
		ipdata = (int(data[0]),str(_ip.network_address),"Network Address")
		sql = ''' INSERT INTO ips(subnetid,IP,Note)
              VALUES(?,?,?) '''
		cur = self.conn.cursor()
		cur.execute(sql, ipdata)
		self.conn.commit()
		
		
		for x in _ip.hosts():
			ipdata = (int(data[0]),str(x))
			sql = ''' INSERT INTO ips(subnetid,IP)
              VALUES(?,?) '''
			cur = self.conn.cursor()
			cur.execute(sql, ipdata)
			self.conn.commit()
			
		#create broadcast address entry
		ipdata = (int(data[0]),str(_ip.broadcast_address),"Broadcast Address")
		sql = ''' INSERT INTO ips(subnetid,IP,Note)
              VALUES(?,?,?) '''
		cur = self.conn.cursor()
		cur.execute(sql, ipdata)
		self.conn.commit()
			
	def get_ips(self, subnetid):
		cur = self.conn.cursor()
		cur.execute("SELECT IP,Status,Hostname,Note FROM ips where subnetid='"+str(subnetid)+"'")
 
		rows = cur.fetchall()
		return rows
	def get_subnet_id(self, name):
		cur = self.conn.cursor()
		cur.execute("SELECT id FROM subnets where name='"+name+"'")
 
		rows = cur.fetchall()
		return rows[0][0]
		
	def get_subnets(self):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM subnets")
 
		rows = cur.fetchall()
		
		for row in rows:
			self.subnets.append(row[1])
		
		
	def update_ip_hostname(self,data):
		
		sql = ''' UPDATE ips set Hostname=? where IP=? and subnetid=? '''
		cur = self.conn.cursor()
		cur.execute(sql, data)
		self.conn.commit()
		
	def update_ip_status(self,data):

		sql = ''' UPDATE ips set Status=? where IP=? and subnetid=? '''
		cur = self.conn.cursor()
		cur.execute(sql, data)
		self.conn.commit()
		
	def export_CSV(self, _subnetid, _dir, _filename):
		
		x = datetime.datetime.now()
		_spacer = x.strftime("%f")
		_csvfile = _dir +'/'+_filename+'_'+_spacer+'.csv'
		_ips = self.get_ips(_subnetid)
		
		with open(_csvfile, 'w', newline='', encoding='UTF8') as csvfile:
			fieldnames = ["IP", "Status","Hostname","Note"]
			writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)

			writer.writerow(fieldnames)
			writer.writerows(_ips)

		return _csvfile

	
	def db_close(self):
		self.conn.close()

		
