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
	wsdm[id].append(int(cList[2]))
	
fd = open("qrels/refined/origin502_word2vec_qrel_refine", "r")
contents = fd.readlines()
luna = {}
for c in contents:
	c = c.strip("\n")
	cList = c.split(" ")
	id = cList[0]
	if id not in luna:
		luna[id] = []
	luna[id].append(int(cList[2]))

count_all = 0
count_in = 0
for id in wsdm:
	gold_list = wsdm[id]
	try:
		r = luna[id]
		inter = list(set(r) & set(gold_list))
		print inter
		if len(inter) != 0:
			count_in += 1
		count_all += 1
	except:
		count_all += 1
		pass
print count_in
print count_all
print float(count_in)/count_all
