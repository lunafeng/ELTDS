#!/usr/bin/python
import MySQLdb,os,time
import getId,getDistribution
from pyspark import SparkContext

db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')

# Get top n related words for each spot according to its distribution
def checkExist(word):
	if os.path.exists("topN/" + word + "_Top" + str(n)):
		return True
	else:
		return False

def main(word):
	print "Start:",word
	wordId = getId.main(word)
	if wordId != None:
		distributionList = getDistribution.main(wordId)
	else:	
		distributionList = []
	vector = {}
	for i in range(len(distributionList)):
		vector[i+1] = distributionList[i]
	words = vector.keys()
	values = vector.values()
	values.sort(reverse=True)
	fd2 = open("topN/" + word +"_Top" + str(n),"a+")
	if len(values) > 0:
		for i in range(n):
			if float(values[i]) != float(0):
				id = vector.keys()[vector.values().index(values[i])]
				vector.pop(id)
				word = str(id)
				fd2.write(word)
				fd2.write(",")
				fd2.write(str(values[i]))
				fd2.write("\n")
			else:
				break

global n
n = 2000
sc = SparkContext("local[4]")
spots = open("../DataSets/spots_ambig","r")
contents = spots.readlines()
rows = [c.strip("\n").split(",")[0] for c in contents if c.strip("\n").split(",")[1] == "1"] 
rows = list(set(rows))
wordsAll = []
for row in rows[:2]:
	exist = checkExist(row)
	if exist == False and row not in wordsAll:
		wordsAll.append(row)
r = sc.parallelize(wordsAll)
r.map(main).collect()
