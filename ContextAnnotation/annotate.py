#!/usr/bin/python
import ast
import MySQLdb
from csv import reader

db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
db_mysql.ping()
cursor = db_mysql.cursor()

def main(tweetId,tweetSpots):
		Final = []	
		sql = "SELECT Concept FROM (SELECT * FROM TweetConceptSim_Word2Vec Where TweetId = " + str(tweetId) + " ORDER BY `Sim` DESC, Concept) x GROUP BY `Sense`"
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				Final.append("https://en.wikipedia.org/wiki/" + r[0])
		except:
			pass
		return Final

	

tweetspots = open("../DataSets/original_tweets_spots.csv","r")
spots = open("../DataSets/spots_ambig","r")
output = open("../AnnotateRes/origin502_word2vec", "w+")

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
	annotations = main(tweetId,tweetSpots)
	output.write(str(tweetId) + "\t" + tweet + "\t" + str(annotations) + "\n")
	output.flush()


