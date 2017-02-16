#!/usr/bin/python
import os
import stemming

def main(tweet,tweetSpots):
	wordsFreq = {}
	allWords = []
	spotsWords = []

	tweetWords = tweet.split(" ")
	tweetWords += tweetSpots.keys()
	for word in tweetWords:
		originWord = word
		if "_" not in word:
			word = stemming.main(word)
		else:
			spotsWordsRaw = word.split("_")
			spotsWords = [stemming.main(spotword) for spotword in spotsWordsRaw if stemming.main(spotword) != "" and "http" not in stemming.main(spotword)]
		if word != "" and "http" not in word:
			if "_" not in word:
				allWords.append(word)
		allWords += spotsWords

	for word in allWords:
		if word not in wordsFreq:
			wordsFreq[word] = 1
		else:
			wordsFreq[word] += 1
	total = sum(wordsFreq.values())
	for word in wordsFreq:
		wordsFreq[word] /= float(total)
	return wordsFreq
