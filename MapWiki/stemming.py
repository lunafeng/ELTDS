#!/usr/bin/python
import sys
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def main(word):
	word = re.sub(r'[,.;:!?\n\'\"\t\-()~{}\[\]<>\_!@#$%^&*\/+-/|=]','',word)
	word = word.replace('\\','')
	try:
		ps = PorterStemmer()
		word = word.lower()
		word = ps.stem(word)
		if word not in stopwords.words("english"):
			return word
		else:
			return ""
	except:
		return ""


