#Animesh Agrawal    animesha    50254531
#Micheal Kirk       kirkmc      49847974
#Rachel Lam         rslam       24554220

import json
import os
from corpus import Corpus
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import math
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

class Inverter:
    """
    This class creates an inverted index of all tokens extracted from the given urls
    """
    def __init__(self):
        self.corpus = Corpus()
        self.wordCountDict = defaultdict(dict)
        self.documentFrequencyDict = dict()
        self.tfidfDict = defaultdict(dict)
        self.lemmatizer = WordNetLemmatizer()
        self.stopWords = set(stopwords.words('english'))
        self.porterStemmer = PorterStemmer()
        self.KEYWORDS = dict()
        self.h2key = dict()
        self.h3key = dict()
        self.h4key = dict()
        
    def calculate_word_count(self, url, url_text):
        ''' This function takes in a url and the html text component and creates tokens and counts the number of time
            a token appeared in the URL
            TF in TF-IDF'''
        wordCountDict = defaultdict(int) #count number of words, used to calculate td-idf
        total_num_words = 0 #used to calculate tf-idf
        
        tokenized = re.split('[^a-zA-z0-9]+', url_text)
        for token in tokenized:
            if token not in self.stopWords:
                token = token.lower() # Changing to lowercase
                token = self.lemmatizer.lemmatize(token) #Lemmatizing each token
                token = self.porterStemmer.stem(token) #Stemming each token
                total_num_words += 1

                if token in self.wordCountDict and url in self.wordCountDict[token]:
                        self.wordCountDict[token][url] += 1
                else:
                    self.wordCountDict[token][url] = 1

    def calculate_document_frequency(self):
        '''Calculating how many documents each token occors in
            IDF in TF_IDF'''
        for term, dictionary in self.wordCountDict.items():
            self.documentFrequencyDict[term] = len(dictionary)

    def calculate_tfidf(self):
        ''' Takes the TF and IDF to combine them to create the TF-IDF score
            H1 and Title adds extra 5points to weight
            H2 adds extra 4points to weight
            H3 adds extra 3points to weight
            H4 adds extra 2points to weight'''
        print(self.corpus.get_corpus_length())
        for term, dictionary in self.wordCountDict.items():
            for url, freq in dictionary.items():
                # Weight = (1+log(TF) * log(corpus_size/IDF))
                weight = (1 + math.log(freq)) * (math.log(self.corpus.get_corpus_length()/self.documentFrequencyDict[term]))
                self.tfidfDict[term][url] = weight
                if term in self.KEYWORDS and url in self.KEYWORDS[term]:
                    self.tfidfDict[term][url] += 5
                if term in self.h2key and url in self.h2key[term]:
                    self.tfidfDict[term][url] += 4
                if term in self.h3key and url in self.h3key[term]:
                    self.tfidfDict[term][url] += 3
                if term in self.h4key and url in self.h4key[term]:
                    self.tfidfDict[term][url] += 2

    def fix_keywords(self, keyword_string):
        '''Takes in a string and breaks it into tokens and standardizes them and returns a set of these tokens'''
        l = set()
        s = re.sub(r'[^a-zA-Z0-9]+', ' ', keyword_string)
        s = s.split(' ')
        if len(s) > 0:
            for word in s:
                word = word.strip()
                word = word.lower()
                word = self.lemmatizer.lemmatize(word)
                word = self.porterStemmer.stem(word)
                if word != '':
                    l.add(word)
        return l
        
    def get_html_text(self, url, url_file):
        '''Takes a URL and the local path to the file, extracts H1, H2, h3, h4, Title and All the html tags and
            saves the data to respective dictionaries and datastructure to be tokenized and used to create index later'''
        f = open(url_file, "rb")
        content = f.read()
        soup = BeautifulSoup(content, "lxml")

        #get rid of all the script stuff
        for script in soup(["script", "style"]):
            script.extract()

        keys = ''
        h2keys = ''
        h3keys = ''
        h4keys = ''
        for content in soup.find_all('title'):
            content = content.get_text()
            keys += content + " "

        for content in soup.find_all('h1'):
            content = content.get_text()
            keys += content + " "

        for content in soup.find_all('h2'):
            content = content.get_text()
            h2keys += content + " "

        for content in soup.find_all('h3'):
            content = content.get_text()
            h3keys += content + " "

        for content in soup.find_all('h4'):
            content = content.get_text()
            h4keys += content + " "


        key_set = self.fix_keywords(keys)
        h2keys = self.fix_keywords(h2keys)
        h3keys = self.fix_keywords(h3keys)
        h4keys = self.fix_keywords(h4keys)

        for key in h2keys:
            if key in self.h2key.keys():
                self.h2key[key].append(url)
            else:
                self.h2key[key] = [url]

        for key in h3keys:
            if key in self.h3key.keys():
                self.h3key[key].append(url)
            else:
                self.h3key[key] = [url]

        for key in h4keys:
            if key in self.h4key.keys():
                self.h4key[key].append(url)
            else:
                self.h4key[key] = [url]


        for key in key_set:
            if key in self.KEYWORDS.keys():
                self.KEYWORDS[key].append(url)
            else:
                self.KEYWORDS[key] = [url]

        #get the rest of the url text
        url_text = soup.get_text()
        lines = (line.strip() for line in url_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        url_text = '\n'.join(chunk for chunk in chunks if chunk)

        return (url, url_text)

    def start_indexing(self):
        '''
            Reads the bookkeeping JSON and creates index for each of the URLs in the JSON file
        '''
        #using good.txt from WebCrawler instead of going through the whole corpus
        counter = 0
        # The corpus directory name
        WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
        # The corpus JSON mapping file
        JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")
        file_url_map = json.load(open(JSON_FILE_NAME), encoding="utf-8")
        #print(file_url_map)
        for loc, url in file_url_map.items():
            url = url.strip()
            loc = loc.split("/")
            dir = loc[0]
            file = loc[1]
            url_file = os.path.join(".", WEBPAGES_RAW_NAME, dir, file)
            if url_file is not None:
                counter += 1
                print(url, "---------", counter)
                url, url_text = self.get_html_text(url, url_file)
                self.calculate_word_count(url, url_text)
    
    def get_wordCountDict(self):
        '''Prints TF for each term'''
        for key, val in self.wordCountDict.items():
            docFreqPair = sorted(val.items(), key = lambda x: x[1], reverse = True)
            print(key, docFreqPair)

    def get_documentFrequencyDict(self):
        '''Prints the IDF for each term'''
        for key, val in self.documentFrequencyDict.items():
            print(key, val)

    def get_tfidfDict(self):
        '''Returns the TF-IDF for each term in a Dictionary'''
        for key, val in self.tfidfDict.items():
            docFreqPair = sorted(val.items(), key = lambda x: x[1], reverse = True)
            #print(key, docFreqPair, "\n\n")
        return self.tfidfDict

if __name__ == '__main__':
    i = Inverter()
    i.start_indexing()
    i.calculate_document_frequency()
    i.calculate_tfidf()
    inverted = i.get_tfidfDict()
    with open('invertedIndex.json', 'w') as f: #saving the TF-IDF dict in a JSON file for later use
        json.dump(inverted, f)

