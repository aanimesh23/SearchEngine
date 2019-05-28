import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

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
    	json_file = open()
    	json_str = json_file.read(filename)
    	json.dict = json.loads(json_str)[0]
    	self.invertedIndex = json.dict

    def retreive_urls(self, query):
    	url_scores = defaultdict(float)
        tokenized = re.split('[^a-zA-z0-9]+', url_text)
        for token in tokenized:
            if token not in self.stopWords:
                token = token.lower()
                token = self.lemmatizer.lemmatize(token)
                token = self.porterStemmer.stem(token)
            	if token in self.tfidfDict.keys():
                	for url, tfidf in self.tfidfDict[token].items():
                    	url_scores[url] += tfidf

        url_scores = sorted(url_scores.items(), key = lambda x: x[1], reverse = True)
        self.sorted_urls = url_scores

    def get_top_urls(self):
    	urlLength = len(sorted_urls)
    	if urlLength < 20:
    		print(sorted_urls)
    	else:
    		i = 1
    		while i <= 20:
	    		for url,value in self.sorted_urls.items():
	    			print(i, url)
	    			i+=1