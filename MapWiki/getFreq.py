#!/usr/bin/python
import stemming
import wikipedia
import getAmbiguousPages

def main(title):
	documents = getAmbiguousPages.main(title) 
	wikiVector_hash = {}
	for c in documents:
			wikiTitle = c.capitalize()
			wikiTitle = wikiTitle.replace("(", "\(")
			wikiTitle = wikiTitle.replace(")", "\)")
			wikiTitle = wikiTitle.replace("_", " ")
			wordsFreq = {}
			try:
					p = wikipedia.page(wikiTitle)
					content = p.content

					extractList = content.split(" ")
					extractStemmedList = []
					for word in extractList:
						word = stemming.main(word)
						if word != "":
							extractStemmedList.append(word)
					for word in extractStemmedList:
						if word not in wordsFreq:
							wordsFreq[word] = 1
						else:
							wordsFreq[word] += 1
					total = len(extractStemmedList)
					for word in wordsFreq:
						wordsFreq[word] /= float(total)
				
			except:
				pass
			wikiVector_hash[c] = wordsFreq
	return wikiVector_hash

