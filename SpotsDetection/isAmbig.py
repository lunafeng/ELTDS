#!/usr/bin/python
import wikipedia
import urllib

def main(word):
	url = "https://en.wikipedia.org/wiki/" + str(word) + "_(disambiguation)"
	try:
		p = urllib.urlopen(url)
		c = p.read()
		s = "Wikipedia does not have an article with this exact name."
		return s not in c 
	except:
		return False

