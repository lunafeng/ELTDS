#!/usr/bin/python
import math
import MySQLdb
import enchant
import os, sys
from os import listdir
from nltk.corpus import wordnet as wn

db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')

def checkExist(givenWord, n):
	if  os.path.exists("filtered/" + givenWord  + "_Keep" + str(n)):
		return True
	else:
		return False

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

def getTfIdf(givenDoc):
	docContentHash = docsHash[givenDoc + "_Top" + str(topn)]
	docTfIdfHash = {}	
	for word in docContentHash:
		tf = docContentHash[word]
		inf = 0
		for doc in docsHash:
			docHash = docsHash[doc]
			if word in docHash:
				inf += docHash[word]
		try:
			idf = math.log10(float(1) / inf)
			docTfIdfHash[word] = float(tf * idf)
		except:
			pass
	return docTfIdfHash

def getTopN(givenDoc, N, docTfIdfHash):
	nouns = {x.name().split('.',1)[0] for x in wn.all_synsets('n')}
	d = enchant.Dict("en_US")
	fd = open("filtered/" + givenDoc  + "_Top300", "w+")
	values = docTfIdfHash.values()
	values.sort(reverse=True)
	topN = 0
	for value in values:
		if topN < N:
			wordId = docTfIdfHash.keys()[docTfIdfHash.values().index(value)]
			word = getWord(wordId)
			try:
				if not "http" in word.lower() and not "www" in word.lower() and not any(i.isdigit() for i in word):
					if "_" not in word:
						if word.lower() in nouns or word in spotsList:
							fd.write(str(wordId) + "\n")
							docTfIdfHash.pop(wordId)
							topN += 1
					else:
						fd.write(str(wordId) + "\n")
						docTfIdfHash.pop(wordId)
						topN += 1
				sys.stdout.flush()
			except:
				pass

global docsList, docNum, doscHash
global spotsList
global topn, keepn
topn = 2000
keepn = 300
spotsList = []

filePath = "topN/"
docsList = [f for f in listdir(filePath)]
docNum = len(docsList)
docsHash = {}
for doc in docsList:
	fd = open(filePath + doc,"r")
	contents = fd.readlines()
	docContentHash = {}
	if doc.endswith("_Top" + str(topn)):
		for c in contents:
			c = c.strip("\n")
			cList = c.split(",")
			word = cList[0]
			value = cList[1]
			try:
				docContentHash[word] = float(value)
			except:	
				docContentHash[word] = float(0)
		docsHash[doc] = docContentHash

fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
raws = [c.strip("\n").split(",")[0] for c in contents if c.strip("\n").split(",")[1] == "1"]
for raw in raws:
	spotsList.append(raw)

for givenDoc in spotsList:
	exist = checkExist(givenDoc, keepn)
	if exist == False and givenDoc != "":
		docTfIdfHash =  getTfIdf(givenDoc)
		getTopN(givenDoc, keepn, docTfIdfHash)


	
