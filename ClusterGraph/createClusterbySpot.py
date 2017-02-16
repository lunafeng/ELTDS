#!/usr/bin/python
import os
import json
import ast
import community
import networkx as nx

def cluster(givenWord):
		clusters = {}
		try:
				g = nx.read_edgelist("../CreateGraph/graphs_word2vec/" + givenWord + "_Top" + str(top) + ".gh")
				partition = community.best_partition(g)
				print "partition:",partition
				for i in set(partition.values()):
					members = list_nodes = [str(nodes) for nodes in partition.keys() if partition[nodes] == i]
					clusters[str(i)] =  members  
				return clusters
		except:
			return None

global top
top = 300
fd = open("../DataSets/spots_ambig","r")
contents = fd.readlines()
raws = [c.strip("\n").split(",")[0] for c in contents if int(c.strip("\n").split(",")[1]) == 1]
raws = list(set(raws))
for word in raws:
		communities = {}
		givenWord = word
		if not os.path.exists("wordClusters_word2vec/" + givenWord + ".json"):
				print givenWord
				clusters = cluster(givenWord)
				if clusters != None:
					communities[str(word)] = clusters
				comNew = json.dumps(communities)
				fd = open("wordClusters_word2vec/"+ givenWord + ".json","w")
				fd.write(comNew)
