from gensim.models import Word2Vec

model = Word2Vec.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

def main(word1, word2):
	try:
		return model.similarity(word1, word2)
	except:
		return 0

