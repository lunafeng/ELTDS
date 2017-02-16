#!/usr/bin/python
import json
import stemming

def removeDuplicates(spot, urlHash): 
		urlHashNew = {}
		values = urlHash.values()
		valuesNew = list(set(values))
		try:
			valuesNew.remove(None)
		except:
			pass
		valuesNew = [v for v in valuesNew if not v.startswith("https://en.wikipedia.org/wiki/All_pages_beginning_with") and not v.startswith("https://en.wikipedia.org/wiki/Category:")]
		for i in range(len(valuesNew)):
			key = spot + "_" + str(i)
			urlHashNew[key] = valuesNew[i]
		return urlHashNew


def main(spotsList):
		wikiConcepts = {}
		tweetSpots = []
		path = "../MapWiki/senses_word2vec/"
		for spot in spotsList:
				try:
						urlHash = json.load(open(path + spot + "_wikiConcepts.json", "r"))
						urlHashNew = removeDuplicates(spot, urlHash)
						if len(urlHashNew) != 0:
							wikiConcepts.update(urlHashNew)
							tweetSpots.append(spot)
						else:
							wikiConcepts[spot + "_0"] = "https://en.wikipedia.org/wiki/" + spot 
							tweetSpots.append(spot)
				except:
				  	pass
		return (wikiConcepts, tweetSpots)
