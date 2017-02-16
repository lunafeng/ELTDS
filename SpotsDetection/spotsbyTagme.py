import ast
import urllib
import string
import enchant
import validWiki
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

d = enchant.Dict("en_US")
tknzr = TweetTokenizer()
punc = string.punctuation
letter = string.ascii_letters
stop = stopwords.words('english')
tagme_url = '''http://tagme.d4science.org/tagme/spot?gcube-token=3b060dff-25be-40c9-bee2-1624c786ea05-843339462&lang=en&text='''

def cleanTweet(row):
	new_tweet = ""
	origin_tweet = row["text"]	
	annotations = ast.literal_eval(row["annotations"])	
	if "-" not in annotations:
		tokens = tknzr.tokenize(origin_tweet)
		for t in tokens:
			if not t.startswith("http") and t not in punc:
				if t.startswith("@"):
					t = t[1:]
				if "-" in t:
					words = t.split("-")
					for w in words:
						if w not in punc:
							new_tweet += " " + w.lower() 
				new_tweet += " " + t 
	return new_tweet

def findSpots(text):
	spots = []
	text = text.replace("#", "")
	text = text.replace("%", "")
	try:
		tagme_url_input = tagme_url + text
		result = urllib.urlopen(tagme_url_input)
		result = ast.literal_eval(result.read())["spots"]
		for r in result:
			spot = r["spot"]
			if (validWiki.main(spot) is True or 
				validWiki.main(spot.title()) is True or 
				validWiki.main(spot.capitalize()) is True):
				spots.append(spot)
			elif " " not in spot and "-" not in spot:
				spot_sug = d.suggest(spot)[0]
				if (validWiki.main(spot_sug) is True or 
					validWiki.main(spot_sug.title()) is True or 
					validWiki.main(spot_sug.capitalize()) is True):
					spots.append(spot_sug)
			if " " in spot or ' ' in spot:
				spot_list = spot.split(" ")
				for s in spot_list:
					if (validWiki.main(s) is True or 
						validWiki.main(s.title()) is True or 
						validWiki.main(s.capitalize()) is True):
						spots.append(s)
		spots = list(set(spots))
		for s in spots:
			if s in letter and s in stop: 
				spots.remove(s)
	except:
		pass
	return spots

tweets_data = pd.read_csv("../GoldStandard/original_tweets_annotations.list", delimiter="\t")
tweets_data["cleaned_tweets"] = tweets_data.apply(cleanTweet, axis = 1)
tweets_data["spots"] = tweets_data["cleaned_tweets"].apply(findSpots)
tweets_spots = tweets_data[["tweetid","text","spots"]]
tweets_spots.to_csv("original_tweets_spots.csv",index=False)
