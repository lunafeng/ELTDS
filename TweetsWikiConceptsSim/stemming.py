#!/usr/bin/python
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import sys
import re

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
