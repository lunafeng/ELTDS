#!/usr/bin/python
fd = open("../GoldStandard/wsdm2012_qrels.txt", "r")
contents = fd.readlines()
wsdm = {}
for c in contents:
	c = c.strip("\n")
	cList = c.split(" ")
	id = cList[0]
	if id not in wsdm:
		wsdm[id] = []
	wsdm[id].append(cList[2])
	

fd = open("qrels/origin502_word2vec_qrel", "r")
contents = fd.readlines()
luna = {}
for c in contents:
	c = c.strip("\n")
	cList = c.split(" ")
	id = cList[0]
	if id not in luna:
		luna[id] = []
	luna[id].append(cList[2])


fd2 = open("qrels/refined/origin502_word2vec_qrel_refine", "w+")
for id in wsdm:
	gold_list = wsdm[id]
	try:
		r = list(set(luna[id]))
		inter = list(set(r) & set(gold_list))
		count = len(r)
		for conceptid in inter:
			fd2.write(str(id) + " 0 " + str(conceptid) + " 0 " +  str(count) + " 0\n")
			count -= 1
		for conceptid in r:
			if conceptid not in inter:
				fd2.write(str(id) + " 0 " + str(conceptid) + " 0 " +  str(count) + " 0\n")
				count -= 1
	except:
		pass
