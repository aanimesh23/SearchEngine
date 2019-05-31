#Animesh Agrawal    animesha    50254531
#Micheal Kirk       kirkmc      49847974
#Rachel Lam         rslam       24554220

import json
from corpus import Corpus
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import defaultdict
import re

class Retreiver:
    """
    This class creates an inverted index of all tokens extracted from the given urls
    """
    def __init__(self):
        self.corpus = Corpus()
        self.invertedIndex = {}
        self.sorted_urls = {}
        self.lemmatizer = WordNetLemmatizer()
        self.stopWords = set(stopwords.words('english'))
        self.porterStemmer = PorterStemmer()

    def open_inverted_index(self, filename):
        '''Reads a inverted index JSON file and stores it a dictionary'''
        json_file = open(filename)
        json_str = json_file.read()
        json.dict = json.loads(json_str)
        self.invertedIndex = json.dict

    def retreive_urls(self, query):
        '''
            Given a text query, it finds the relevant URLs in the index and returns a list of top URLs in a
            decreasing order of TF-IDF scores for each URL for the Query
        '''
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
        return url_scores

    def get_top_urls(self, sorted_urls, max = 20):
        '''
            Prints the top URLs that are retrived with thier TF-IDF values
            Defaults to top 20 urls but can be changed
        '''
        urlLength = len(sorted_urls)
        if urlLength < max:
            print(sorted_urls)
        else:
            i = 1
            for url,value in sorted_urls:
                if (i <= max):
                    print(i, url, "------------", value)
                    i+=1
                else:
                    break

    def list_top_urls(self, query):
        '''
            Retriever API, Used for extrenal Programs
            This function takes in a Query and returns a 2-Tuple containing list of top 20 URLs and the length of the list 
        '''
        top_urls = []
        max_urls = 20
        sorted_urls = self.retreive_urls(query)
        url_length = len(sorted_urls)
        
        if url_length < max_urls:
            for url, value in sorted_urls:
                top_urls.append(url)
        else:
            i = 0
            for url, value in sorted_urls:
                if (i < max_urls):
                    top_urls.append(url)
                    i += 1
                else:
                    break
        return top_urls, len(top_urls)
        

    def queries(self):
        '''
            A UI function that asks a user for an input query and prints top 20 URLs on the terminal
        '''
        while True:
            s = str(input("Input Search Query\n"))
            if s == '':
                continue
            if s == ' ':
                continue
            if s == 'exit':
                break
            l = r.retreive_urls(s)
            r.get_top_urls(l)
            print("\n\n")



if __name__ == '__main__':
    r = Retreiver()
    r.open_inverted_index("invertedIndex.json")
    r.queries()
