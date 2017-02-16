#!/usr/bin/python
import ast
import docSim
import MySQLdb
import stemming
import getWikiVector
import getTweetVector
from csv import reader
import getWikiConcepts
db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
cursor = db_mysql.cursor()

def main(tweetId, tweet, tweetSpots):
	db_mysql.ping()
	ambiSpots = [spot for spot in tweetSpots if tweetSpots[spot] == 1]
	disambiSpots = [spot for spot in tweetSpots if tweetSpots[spot] == 0]
	tweetVector = getTweetVector.main(tweet,tweetSpots)
	results =  getWikiConcepts.main(ambiSpots)
	wikiConcepts = results[0]

	for spot in disambiSpots:
		wikiConcepts[spot + "_0"] = "https://en.wikipedia.org/wiki/" + spot

	for sense in wikiConcepts:
		store = ""
		url = wikiConcepts[sense]	
		if url != None:
			titleList = wikiConcepts[sense].split("/wiki/")	
			wikiVector = getWikiVector.main(titleList[1])
			result = docSim.main(tweet, wikiVector)
			result = result * len(wikiVector.split(" ")) ** 0.8
			senseList = sense.split("_")
			senseName = "_".join(senseList[:-1])
			senseId = senseList[-1]
			titleNew = str(titleList[1]).encode('string-escape')
			store += "(" + str(tweetId) + "," + str(senseId) + ",\'" + str(senseName) + "\',\'" + titleNew + "\'," + str(result) + ")"
			sql = "INSERT IGNORE INTO TweetConceptSim_Word2Vec(TweetId, SenseId, Sense, Concept, Sim) VALUES " + store
			try:
				cursor.execute(sql)
				db_mysql.commit()
			except:		
				db_mysql.rollback()
		
		


tweetspots = open("../DataSets/original_tweets_spots.csv","r")
spots = open("../DataSets/spots_ambig","r")
spotsHash = {}
spotscontents = spots.readlines() 
for spot in spotscontents:
	spot = spot.strip("\n")
	spotList = spot.split(",")
	spotsHash[spotList[0]] = int(spotList[1])

head = 0
for line in reader(tweetspots):
	if head == 0:
		head += 1
		continue
	tweetSpots = {}
	tweet = line[1]
	tweetId = int(line[0])
	spots = ast.literal_eval(line[2])
	for spot in spots:
		spot = spot.lower()
		spot = spot.replace(" ", "_")
		tweetSpots[spot] = spotsHash[spot]
	print tweetId
	main(tweetId, tweet, tweetSpots)
