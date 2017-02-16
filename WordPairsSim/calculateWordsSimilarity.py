#!/usr/bin/python

def main(list1,list2):
	top = 0.0
	bottom1 = 0.0
	bottom2 = 0.0
	try:
		for i in range(len(list1)):
			try:
				value1 = float(list1[i])
				value2 = float(list2[i])
				top = top + value1*value2
			except:
				pass
		for i in range(len(list1)):
			try:
				bottom1 = bottom1 + float(list1[i])**2
			except:
				pass
		for i in range(len(list2)):
			try:
				bottom2 = bottom2 + float(list2[i])**2
			except:
				pass
		return top/(bottom1*bottom2)**0.5
	except:
		return float(0)
