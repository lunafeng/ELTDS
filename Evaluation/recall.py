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
			intersect = list(set(gold_list) & set(r))
			print "intersect:", len(intersect)
			print "gold:", len(gold_list)
			count_in += len(intersect)
			count_all += len(gold_list)
	except:
			count_all += len(gold_list)

print count_in
print count_all
print float(count_in)/count_all
