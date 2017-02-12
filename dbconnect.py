#connecting our mysql database to the application

import MySQLdb

def connection():
	conn = MySQLdb.connect(host='localhost', user = 'root', passwd ="dama", db= 'users_directory')
	c = conn.cursor()
	return c, conn