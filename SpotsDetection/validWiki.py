import urllib
import wikipedia
from itertools import permutations

def main(title):
	url1 = "https://en.wikipedia.org/wiki/" + title
	url2 = "https://en.wikipedia.org/wiki/" + title + "_(disambiguation)"
	p1 = urllib.urlopen(url1)
	p2 = urllib.urlopen(url2)
	c1 = p1.read()
	c2 = p2.read()
	s = "Wikipedia does not have an article with this exact name."
	if s not in c1 or s not in c2:
		return True
	else:
		return False
			

