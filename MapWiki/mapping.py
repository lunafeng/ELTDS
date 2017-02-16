#!/usr/bin/python
import os
import json
import getFreq
import stemming

fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
for c in contents:
	communities = {}
	c = c.strip("\n")
	cList = c.split(",")
	wordAm = cList[0]
	ambig = cList[1]
	if not os.path.exists("senses_word2vec/" + wordAm + "_wikiConcepts.json") and int(ambig) == 1:
			wikiConcepts = {}
			try:
					senses = json.load(open("../ClusterGraph/wordClusters_word2vec/" + wordAm + ".json", "r"))[wordAm]
					tfidf = getFreq.main(wordAm)
					for senseId in senses:
						max = 0
						match = ""
						finalMatch = ""
						senseWords = senses[senseId]
						for article in tfidf:
							sum = 0
							count = 0
							tfidfwords = tfidf[article] 
							article_length = len(tfidfwords)
							for word in senseWords:
								try:
									if "_" in word:
										wordList = word.split("_")
										for word in wordList:
											if stemming.main(word) in tfidfwords:
												count += 1
									else:
										if stemming.main(word) in tfidfwords:
											count += 1
								except:
									pass
							if article_length != 0:
								sum = float(count)/article_length
							else:
								sum = float(0)
							if sum > max:
								max = sum
								match = article
						if match == "":
							finalMatch = None
						else:
							finalMatch = "https://en.wikipedia.org/wiki/" + match
						wikiConcepts[wordAm + "_" + str(senseId)] = finalMatch
					json.dump(wikiConcepts, open("senses_word2vec/" + wordAm + "_wikiConcepts.json", "w"))
			except:
				pass
