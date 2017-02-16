#!/usr/bin/python
import ast
import wikipedia
import MySQLdb
db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')


fd = open("../AnnotateRes/origin502_word2vec", "r")
output = open("qrels/origin502_word2vec_qrel", "w+")
contents = fd.readlines()

for c in contents:
	c = c.strip("\n")
	cList = c.split("\t")
	tweetId = cList[0]
	tweetText = cList[1]
	concepts = ast.literal_eval(cList[2])
	c_result = {}
	for url in concepts:
		urlNew = str(url).encode('string-escape')
		select = "SELECT PageId From WikiPageId WHERE Url=\'" + urlNew + "\'"
		db_mysql.ping()
		cursor = db_mysql.cursor()
		cursor.execute(select)
		result = cursor.fetchone()
		if result == None:
			try:
				title = urlNew.split("/resource/")[1]	
				title = title.replace("_", " ")
				title = title.replace("\"", "")
				page = wikipedia.page(title)
				pageId = page.pageid
				store = "INSERT INTO WikiPageId VALUES (\'" + urlNew + "\'," + str(pageId) + ")"  
				cursor.execute(store)
				db_mysql.commit()
				c_result[pageId] = float(1)
			except:
					pass
		else:
			pageId = result[0]
			c_result[pageId] = float(1)
		cursor.close()
	r_values = c_result.values()
	r_values.sort(reverse=True)
	for v in r_values:
		k = c_result.keys()[c_result.values().index(v)]
		output.write(tweetId + " 0 " + str(k) + " 0 " + str(v) + " 0\n")
		output.flush()
		c_result.pop(k)
