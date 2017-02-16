#!/usr/bin/python
import MySQLdb
import sys,time,os

db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
def main(givenWord, filtern):
		wordNumberHash = {}
		wordsId_list = []
		print givenWord
		#if os.path.exists("../CreateDistr/filtered/" + givenWord + "_Top" + str(filtern)):
		if os.path.exists("/data/CikmTwitterProject/WordsDisambiguation/words-disambiguation/Branches/b4/Filter/FilteredEnglish/" + givenWord + "_Top" + str(filtern)):
				#fd = open("../CreateDistr/filtered/" + givenWord + "_Top" + str(filtern), "r")
				fd = open("/data/CikmTwitterProject/WordsDisambiguation/words-disambiguation/Branches/b4/Filter/FilteredEnglish/" + givenWord + "_Top" + str(filtern), "r")
				resultsRaw = fd.readlines()
				if not os.path.exists("graphs_word2vec/" + givenWord + "_Top" + str(filtern) + ".gh"):
						fdGraph = open("graphs_word2vec/" + givenWord + "_Top" + str(filtern) + ".gh","w+")
						for result in resultsRaw:
							wordId = int(result.strip("\n"))
							if wordId != None:
								wordsId_list.append(wordId)
						search = "("
						for id in wordsId_list:
							search += str(id) + ","
						search = search[:-1]
						search += ")"
						db_mysql.ping()
						cursor = db_mysql.cursor()
						sql = '''SELECT B.Word1,
        						W1.Word AS Word2,
        						B.Similarity
								FROM Words W1
								JOIN
								((SELECT W.Word AS Word1,
										A.Word2,
										A.Similarity
								FROM 
								(SELECT Word1,
										Word2,
										Similarity
								FROM WordsSimilarityWord2Vec 
								WHERE Word1 in %s 
								AND Word2 in %s) A
								JOIN Words W 
								ON (A.Word1 = W.Id)) B)
								ON (W1.Id = B.Word2)''' % (search, search)
						try:
								cursor.execute(sql)
								results = cursor.fetchall()
								for r in results:
									word1 = r[0]
									word2 = r[1]
									if " " in word1:
										word1 = word1.replace(" ","_")
									if " " in word2:
										word2 = word2.replace(" ","_")
									sim = float(r[2])
									if sim != 0:
										fdGraph.write(unicode(str(word1),"utf-8") + " " + unicode(str(word2),"utf-8") + " {\"weight\":" + str(sim) + "}\n")
										fdGraph.flush()
						except:
							pass


fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
raws = [c.strip("\n").split(",")[0] for c in contents if int(c.strip("\n").split(",")[1]) == 1]
for givenWord in raws:
	print "Start:", givenWord
	main(givenWord,300)
	print "Done!"
	sys.stdout.flush()
