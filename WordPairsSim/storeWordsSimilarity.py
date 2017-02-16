#!/usr/bin/python
import time
import MySQLdb

def main(storeValues):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	sql1 = "INSERT IGNORE INTO WordsSimilarityNew(Word1,Word2,Similarity) VALUES " + storeValues
	sql2 = "INSERT IGNORE INTO WordsSimilarityNew(Word2,Word1,Similarity) VALUES " + storeValues
	cursor.execute(sql1)
	db_mysql.commit()
	cursor.execute(sql2)
	db_mysql.commit()
	cursor.close()
	db_mysql.close()
	time.sleep(0.05)


