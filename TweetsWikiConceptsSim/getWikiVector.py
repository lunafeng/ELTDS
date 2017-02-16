#!/usr/bin/python
import wikipedia

def main(c):
	wikiTitle = c.capitalize()
	wikiTitle = wikiTitle.replace("(", "\(")
	wikiTitle = wikiTitle.replace(")", "\)")
	wikiTitle = wikiTitle.replace("_", " ")
	wordsFreq = {}
	content = ""
	try:
		p = wikipedia.page(wikiTitle)
		content = p.summary
	except:
		pass
	return content

