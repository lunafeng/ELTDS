#!/usr/bin/python
import time

def main(word):
	distributionList = []
	try:
		fd = open("distributions/" + str(word) + ".List", "r")
		contents = fd.readlines()
		for content in contents:
			content = content.strip("\n")
			try:
				distributionList.append(float(content))
			except:
				distributionList.append(float(0))
	except:
		pass
	return distributionList


	
