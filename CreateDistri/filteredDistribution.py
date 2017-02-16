#!/usr/bin/python
import json
import getId
import MySQLdb
import os,sys,time
import calDistribution
from pyspark import SparkContext

# get words' distribution from the top n related words with each spot	

def main(givenWord):
	wordId = getId.main(givenWord)
	wordsAll = []
	if  os.path.exists("filtered/" + givenWord + "_Top" + str(n)):
		top = open("filtered/" + givenWord + "_Top" + str(n),"r")
		rawList = top.readlines()
		for raw in rawList:
			wordId = raw.strip("\n")
			if not os.path.exists("distributions/" + str(wordId) + ".List"):
				wordsAll.append(wordId)
	return wordsAll


global n
n = 300
fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
raws = [c.strip("\n").split(",")[0] for c in contents if int(c.strip("\n").split(",")[1]) == 1]

wordsAll = []
for raw in raws:
	words = main(raw)
	wordsAll = list(set(wordsAll + words))

sc = SparkContext("local[4]")
sc.parallelize(wordsAll).map(calDistribution.main).collect()
