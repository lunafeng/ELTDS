#!/usr/bin/python
import json
import os,sys
import MySQLdb
from itertools import combinations

# Store all the word pairs needed to get similarity
def store(all):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	insert = "INSERT IGNORE INTO WordsSimilarityExpect(Word1,Word2) Values " + all
	cursor.execute(insert)
	db_mysql.commit()

def main(givenWord):
	global wordsId_list
	wordsId_list = []
	if os.path.exists("../CreateDistri/filtered/" + givenWord + "_Top" + str(keepn300)):
		fd = open("../CreateDistri/filtered/" + givenWord + "_Top" + str(keepn), "r")
		resultsRaw = fd.readlines()
		for result in resultsRaw:
			wordId = int(result.strip("\n"))
			if wordId != None:
				wordsId_list.append(wordId)
		combinationsRaw = list(combinations(wordsId_list,2))
		all = ""
		for com in combinationsRaw:
			all += str(com) + ","
		all = all[:-1]
		if len(all) != 0:
			store(all)
		print "Done"

global keepn
keepn = 300
fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
raws = [c.strip("\n").split(",")[0] for c in contents if int(c.strip("\n").split(",")[1]) == 1]
for raw in raws:
	print "Start:",raw
	main(raw)
	print raw, " is Done"
	sys.stdout.flush()
