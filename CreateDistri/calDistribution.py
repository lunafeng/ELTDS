#!/usr/bin/python
import os
import sys
import math
import json
import getId
import re,time
import MySQLdb
import subprocess


def stationary_dist(word1,matrix_hash,element_list,walkNumber):
	#initialization
	v0_hash = {}
	for item in element_list:
		if item == word1:
			v0_hash[int(item)] = 1
		else:
			v0_hash[int(item)] = 0

	#v(t) = beta*v(0)+(1-beta)*M*v(t-1)
	vt1_hash = {}
	vt2_hash = {}
	vt1_hash = v0_hash.copy()
	middle_hash = {}
			
	beta = 0.3
	count = 0	
	while(1):
		count += 1
		for element in element_list:
			sum_prob = 0
			to_hash = matrix_hash[str(element)]
			for word in to_hash:	
				sum_prob += float(to_hash[str(word)]) * float(vt1_hash[int(word)])
			middle_hash[int(element)] = sum_prob
				

		value1 = value(vt1_hash.values())

		for element in element_list:
			a = beta * float(v0_hash[int(element)]) + (1 - beta) * float(middle_hash[int(element)])
			vt2_hash[int(element)] = a
			
		value2 = value(vt2_hash.values())
		vt1_hash = vt2_hash.copy()
		if count >= walkNumber:
				break;
	return vt2_hash
			
		
def value(elements_list):
	sum_all = 0
	for element in elements_list:
		sum_all += element**2
	return float(sum_all)**0.5



def main(word):
	filePath = "distributions/"
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','WordsDisambiguation_b4')
	try:
		Id1 = int(word)
	except:
		Id1 = getId.main(word)

	if not os.path.exists("distributions/" + str(Id1) + ".List"):
			db_mysql.ping(True)
			cursor = db_mysql.cursor()
			getAllWords = "select Word from TotalOccurrencesAll"
			cursor.execute(getAllWords)
			allWords = cursor.fetchall()
			cursor.close()

			global element_list
			element_list = []
			for element in allWords:
				element_list.append(int(element[0]))
			matrix_hash = json.load(open("../DataSets/MatrixCPNoOneNoCommonNoSame_b4"))
			
			walkNumber = 5
			vector1 = stationary_dist(Id1,matrix_hash,element_list,walkNumber)
			fd = open(filePath + str(Id1) + ".List","w+")
			valueList = []
			# change the number according to the size of word corpus
			for i in range(28498):
				try:
					value = vector1[int(i+1)]
				except:
					value = ''
				fd.write(str(value) + "\n")
				fd.flush()
	db_mysql.close()


