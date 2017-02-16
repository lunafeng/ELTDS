#!/usr/bin/python
import MySQLdb

def main(word):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	try:
		sql = "SELECT Id From Words WHERE Word=" + '\''+word+'\'';
		cursor.execute(sql)
		Id = cursor.fetchone()
	except:
		db_mysql.rollback()
	cursor.close()
	db_mysql.close()
	try:
		return int(Id[0])
	except:
		return None
