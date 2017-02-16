#!/usr/bin/python
import json
import os,sys
import MySQLdb
import subprocess
import storeWordsSimilarity
import calculateWordsSimilarity
from pyspark import SparkContext
from itertools import combinations

db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')

def getWord(id):
	try:
		db_mysql.ping(True)
		cursor = db_mysql.cursor()
		sql = "SELECT Word From Words WHERE Id=" + str(id);
		cursor.execute(sql)
		word = cursor.fetchone()
		cursor.close()
		return word[0]
	except:
		db_mysql.rollback()
		return None

def calculate(word2):
	storeValue = ""
	if word2 != None:
		similarityWord = float(calculateWordsSimilarity.main(word1,word2))
		wordId2 = word2_Id_hash[word2]
		if wordId1 != None and wordId2 != None and type(similarityWord) == float:
			storeValue = "(" + str(wordId1) + "," + str(wordId2) + "," + str(similarityWord) + ")"
	sys.stdout.flush()
	return storeValue

fd = open("../wordPairs","r")
raws = fd.readlines()
wordHash = {}
for raw in raws:
		raw = raw.strip("\n")
		wordList = raw.split("\t")
		word1 = wordList[0]
		word2 = wordList[1]
		if word1 not in wordHash:
			wordHash[word1] = []
			wordHash[word1].append(word2)
		else:
			wordHash[word1].append(word2)

global wordId1
sc = SparkContext("local[8]")
for wordId1 in wordHash:
		print wordId1
		global word1
		global word2_Id_hash
		word1 = getWord(wordId1) 
		wordId2_list = wordHash[wordId1]
		word2_Id_hash = {}
		for wordId2 in wordId2_list:
			word2 = getWord(wordId2)
			word2_Id_hash[word2] = wordId2
		if word1 != None and len(wordHash[wordId1]) != 0:	
			simValues = sc.parallelize(word2_Id_hash.keys()).map(calculate).collect()
			storeValues = ""
			for simValue in simValues:
				if simValue != "":
					storeValues += str(simValue) + ","
			storeValues = storeValues[:-1]
			if storeValues != "":
				storeWordsSimilarity.main(storeValues)
sc.stop()

