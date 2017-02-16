#!/usr/bin/python
import json
import os,sys
import MySQLdb
import subprocess
import storeWordsSimilarity
import getWordDistributionList
import calculateWordsSimilarity
from pyspark import SparkContext
from itertools import combinations


def calculate(wordId2):
	storeValue = ""
	list2 = getWordDistributionList.main(wordId2)
	if len(list2) != 0:
		similarityWord = calculateWordsSimilarity.main(list1,list2)
		print "Similarity is:", similarityWord
		if wordId1 != None and wordId2 != None and type(similarityWord) == float:
			storeValue = "(" + str(wordId1) + "," + str(wordId2) + "," + str(similarityWord) + ")"
	print "Pair Value:",storeValue
	sys.stdout.flush()
	return storeValue

fd = open("wordPairs","r")
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

global vector1
sc = SparkContext("local[36]")
for wordId1 in wordHash:
		global list1
		list1 = getWordDistributionList.main(wordId1)
		if len(list1) != 0 and len(wordHash[wordId1]) != 0:	
			simValues = sc.parallelize(wordHash[wordId1]).map(calculate).collect()
			storeValues = ""
			for simValue in simValues:
				if simValue != "":
					storeValues += str(simValue) + ","
			storeValues = storeValues[:-1]
			if storeValues != "":
				storeWordsSimilarity.main(storeValues)
sc.stop()

