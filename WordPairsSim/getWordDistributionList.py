#!/usr/bin/python
import time
import subprocess

def main(word):
	distributionList = []
	filePath = "../CreateDistri/distributions/"
	try:
		fd = open(filePath + str(word) + ".List", "r")
		contents = fd.readlines()
		for content in contents:
			content = content.strip("\n")
			if content != "":
				distributionList.append(float(content))
			else:
				distributionList.append(float(0))
	except:
		pass
	return distributionList

