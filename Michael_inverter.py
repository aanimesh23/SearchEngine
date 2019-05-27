from corpus import Corpus
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import math

class Inverter:
    """
    This class creates an inverted index of all tokens extracted from the given urls
    """
    def __init__(self):
        self.corpus = Corpus()
        self.wordCountDict = defaultdict(dict)
        self.documentFrequencyDict = dict()
        self.tfidfDict = defaultdict(dict)
        self.invertedDict = defaultdict(dict)
        self.tokenSet = set()
        
    def calculate_word_count(self, url, url_text):
        wordCountDict = defaultdict(int) #count number of words, used to calculate td-idf
        total_num_words = 0 #used to calculate tf-idf
        
        tokenized = re.split('[^a-zA-z0-9]+', url_text)
        for token in tokenized:
            self.tokenSet.add(token)
            token = token.lower()
            total_num_words += 1

            if token in self.wordCountDict and url in self.wordCountDict[token]:
                    self.wordCountDict[token][url] += 1
            else:
                self.wordCountDict[token][url] = 1

    def calculate_document_frequency(self):
        for term, dictionary in self.wordCountDict.items():
            self.documentFrequencyDict[term] = len(dictionary)

    def calculate_tfidf(self):
        for term, dictionary in self.wordCountDict.items():
            for url, freq in dictionary.items():
                weight = (1 + math.log(freq)) * (math.log(self.corpus.get_corpus_length()/self.documentFrequencyDict[term]))
                self.tfidfDict[term][url] = weight

    def fetch_best_urls(self, query):
        tokenized
    
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

        return (url, url_text)

    def start_indexing(self):
        #using good.txt from WebCrawler instead of going through the whole corpus
        good_urls = open("good.txt", "r")
        counter = 0

        for url in good_urls.readlines():
            url = url.strip()
            url_file = self.corpus.get_file_name(url)
            if url_file is not None and counter < 9:
                counter += 1
                print(url)
                url, url_text = self.get_html_text(url, url_file)
                self.calculate_word_count(url, url_text)

    def get_invertedDict(self):
        return self.invertedDict
    
    def get_wordCountDict(self):
        for key, val in self.wordCountDict.items():
            docFreqPair = sorted(val.items(), key = lambda x: x[1], reverse = True)
            print(key, docFreqPair)

    def get_documentFrequencyDict(self):
        for key, val in self.documentFrequencyDict.items():
            print(key, val)

    def get_tfidfDict(self):
        for key, val in self.tfidfDict.items():
            docFreqPair = sorted(val.items(), key = lambda x: x[1], reverse = True)
            print(key, docFreqPair, "\n\n")

if __name__ == '__main__':
    i = Inverter()
    i.start_indexing()
    i.calculate_document_frequency()
    i.calculate_tfidf()
    i.get_tfidfDict()
