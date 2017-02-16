#!/usr/bin/python
import getDistribution

spots = open("../DataSets/spots_ambig","r")
contents = spots.readlines()
words = [c.strip("\n").split(",")[0] for c in contents if c.strip("\n").split(",")[1] == "1"] 
words = list(set(words))
for word in words:
	getDistribution.main(word)
