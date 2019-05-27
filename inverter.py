from corpus import Corpus
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import math
import pickle

class Inverter:
    """
    This class creates an inverted index of all tokens extracted from the given urls
    """
    def __init__(self):
        self.corpus = Corpus()
        self.invertedDict = defaultdict(dict)
        
    def tokenize_file(self, url, url_text):
        #tokenizes the url file, calculates the tf-idf, and stores it in invertedDict
        wordCountDict = defaultdict(int) #count number of words, used to calculate td-idf
        tfidfDict = defaultdict(float) #store the tf-idf in a dictionary and then add to invertedDict
        total_num_words = 0 #used to calculate tf-idf
        
        tokenized = re.split('[^a-zA-z0-9]+', url_text)
        for token in tokenized:
            token = token.lower()
            total_num_words += 1
            
            if token in wordCountDict.keys():
                wordCountDict[token] += 1
            else:
                wordCountDict[token] = 1

        #calculate the tf-idf (math is kinda sketchy rn)
        for word, count in wordCountDict.items():
            tfidfDict[word] = count/total_num_words * math.log(self.corpus.get_corpus_length()/(count + 1))
            
        for token in tokenized:
            self.invertedDict[token.lower()][url] = tfidfDict[token]
    
    def get_html_text(self, url, url_file):
        f = open(url_file, "rb")
        content = f.read()
        soup = BeautifulSoup(content, "lxml")

        #get rid of all the script stuff
        for script in soup(["script", "style"]):
            script.extract()

        #get the rest of the url text
        url_text = soup.get_text()
        lines = (line.strip() for line in url_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        url_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        self.tokenize_file(url, url_text)

    def create_dict(self):
        #using good.txt from WebCrawler instead of going through the whole corpus
        good_urls = open("good.txt", "r")
        
        for url in good_urls.readlines():
            url = url.strip()
            url_file = self.corpus.get_file_name(url)
            if url_file is not None:
                print(url)
                self.get_html_text(url, url_file)

    def get_invertedDict(self):
        return self.invertedDict
        
i = Inverter()
i.create_dict()
inverted = i.get_invertedDict()
with open("invertedIndex.pickle", 'wb') as handle:
    pickle.dump(inverted, handle, protocol=pickle.HIGHEST_PROTOCOL)


