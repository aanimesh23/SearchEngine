import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import defaultdict
import re

class Retreiver:
    """
    This class creates an inverted index of all tokens extracted from the given urls
    """
    def __init__(self):
    	self.invertedIndex = {}
    	self.sorted_urls = {}
    	self.lemmatizer = WordNetLemmatizer()
    	self.stopWords = set(stopwords.words('english'))
    	self.porterStemmer = PorterStemmer()

    def open_inverted_index(self, filename):
    	json_file = open(filename)
    	json_str = json_file.read()
    	json.dict = json.loads(json_str)
    	self.invertedIndex = json.dict

    def retreive_urls(self, query):
    	url_scores = defaultdict(float)
    	tokenized = re.split('[^a-zA-z0-9]+', query)
    	for token in tokenized:
    		if token not in self.stopWords:
    			token = token.lower()
    			token = self.lemmatizer.lemmatize(token)
    			token = self.porterStemmer.stem(token)
    			if token in self.invertedIndex.keys():
    				for url, tfidf in self.invertedIndex[token].items():
    					url_scores[url] += tfidf

    	url_scores = sorted(url_scores.items(), key = lambda x: x[1], reverse = True)
    	self.sorted_urls = url_scores

    def get_top_urls(self):
    	urlLength = len(self.sorted_urls)
    	if urlLength < 20:
    		print(self.sorted_urls)
    	else:
    		i = 1
    		while i <= 20:
	    		for url,value in self.sorted_urls:
	    			print(i, url)
	    			i+=1

r = Retreiver()
r.open_inverted_index("invertedIndex.json")
r.retreive_urls("donald bren")
r.get_top_urls()