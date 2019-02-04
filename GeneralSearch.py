from flask import Flask, redirect, render_template, request, session, abort, url_for
from flaskext.mysql import MySQL
from DBconnection import connection
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from TwitterAPI import TwitterAPI
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
import pprint


class GeneralSearch:

    def __init__(self, clientName):
        self.clientName = clientName
        self.url = 'https://www.google.co.in/search?q={}'.format(self.clientName)
        self.document = ''
        self.textDocument = ''
        self.cleanText = ''
        self.keyWords = {}
        self.GOOGLE_API_KEY = "AIzaSyDVjsiH1KjjI7Wus5imNPXFpdczbR5Iaqg"
        self.GOOGLE_CSE_ID = "002858524502186211496:qscl9gemjug" # Google Custom search engine ID

        try:
            cursor, conn = connection()

            query = "SELECT * from KeyWord"
            cursor.execute(query)

            data = cursor.fetchall()

            for i in range(len(data)):
                self.keyWords[data[i][1]] = 0

            cursor.close()
        except Exception as e:
            print(str(e))



    def twitter_search(self):

        SEARCH_TERM = self.clientName
        PRODUCT = 'fullarchive'
        LABEL = 'TestSMI'
        SANDBOX_CONSUMER_KEY = ''
        SANDBOX_CONSUMER_SECRET = ''
        SANDBOX_TOKEN_KEY = ''
        SANDBOX_TOKEN_SECRECT = ''

        api = TwitterAPI(SANDBOX_CONSUMER_KEY,
                         SANDBOX_CONSUMER_SECRET,
                         SANDBOX_TOKEN_KEY,
                         SANDBOX_TOKEN_SECRECT)

        r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                        {'query': SEARCH_TERM})
        f = open("Twitterresult.txt", "w+")
        for item in r:
            f.write(item['text'] + '\n')
            self.document = self.document + '\n'+ item['text']
            print(item['text'] if 'text' in item else item)

        f.close()

    def google_search(self):
        '''
        This function runs a search by client name on google

        '''


        res = []
        service = build("customsearch", "v1", developerKey=self.GOOGLE_API_KEY)

        res.append(service.cse().list(
            q=self.clientName,
            cx=self.GOOGLE_CSE_ID,
            num=10,
            start=1,
        ).execute())

        #pprint.pprint(res)

        count = 0
        InnerCount = 0
        for each in res:
          print('Length of ITEMS', len(each['items']))

        for each in res:
            for i in range(0, len(each['items'])):
                print('TITLES \n')
                print(each['items'][i]['title'])
                self.document = self.document + '\n' + each['items'][i]['title']
                print('CONTENT \n')
                print(each['items'][i]['snippet'])
                self.document = self.document + '\n' + each['items'][i]['snippet']
        print('AFTER SUM \n'+self.document)

        self.textDocument = sent_tokenize(self.document)
        self.cleanText = [self.cleanDocument(s) for s in self.textDocument]

        self.docInfo = self.createDocuments(self.cleanText)
        self.create_freq_dict(self.cleanText)
        self.calculate_TFIDF()





    def run(self):
        '''
        this function run a search on google and store the result in one string
        '''
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        print('Title')
        for item in soup.select(".r a"):
            print(item.text)
            self.document = self.document + '\n' + item.text


        print('Content')
        for item in soup.select(".g span.st"):
            print(item.text)
            self.document = self.document + '\n' + item.text


        self.textDocument = sent_tokenize(self.document)
        self.cleanText = [self.cleanDocument(s) for s in self.textDocument]

        self.docInfo = self.createDocuments(self.cleanText)

        '''for keys, values in self.keyWords.items():
            print(keys)
            print(values)'''
        self.create_freq_dict(self.cleanText)
        self.calculate_TFIDF()

    def cleanDocument(self, doc):
        '''
        this function clean the search result from any white space and special characters
        :param doc: a string containing the search result
        :return: a clean string
        '''

        # Replace special character with ' '
        str = re.sub('[^\w\s]', '', doc)
        str = re.sub('_', '', str)

        # Change any white space to one space
        str = re.sub('\s+', ' ', str)

        # Remove start and end white space
        str = str.strip()

        return str

    def createDocuments(self, cleanDoc):
        '''
        This function splits the search results into sentance considring each
        sentance as a document
        :param cleanDoc:
        :return:
        '''

        doc_info = []
        i = 0
        for cleanDoc in self.cleanText:
            i += 1
            count = self.countWords(cleanDoc)
            temp = {'doc_id': i, 'doc_length': count}
            doc_info.append(temp)
        return doc_info

    def countWords(self, doc):
        count = 0
        words = word_tokenize(doc)
        for word in words:
            count += 1
        return count

    def create_freq_dict(self, cleanDoc):
        i = 0
        for each in cleanDoc:
            i += 1
            words = word_tokenize(each)
            print('\n', words)
            for word in words:
                word = word.lower()
                if word in self.keyWords:
                    self.keyWords[word] += 1
        for keys, values in self.keyWords.items():
            print(keys)
            print(values)


    def calculate_TFIDF(self):
        '''
        this function calculate the number of keywords appeared form the list
        :param list:
        :return:
        '''

        numOfApearance = 0
        sum_of_frequencies = 0
        max_frequency = 0
        SearchClass = 0
        clientClass = ''
        for keys, values in self.keyWords.items():
            if values > 0 :
                max_frequency = max(self.keyWords.values())
                sum_of_frequencies += values
                numOfApearance += 1
        try:

            SearchClass = ((numOfApearance * max_frequency) / (16))
            #Normalization
            if SearchClass > 1:
                SearchClass = 1
        except ZeroDivisionError :
            SearchClass =0


        if 0.7 < SearchClass <= 1:
            clientClass = 'High'
        elif 0.33 < SearchClass <= 0.7:
            clientClass = 'Medium'
        elif 0 < SearchClass <= 0.33:
            clientClass = 'Low'
        else:
            clientClass = 'Clean'


        print('Number of Words apeared from the list', numOfApearance)
        print('MAX FREQUENCY',max_frequency)
        print('Frequeancy', sum_of_frequencies)
        print('SearchClass Weight', SearchClass)
        print('Client Class', clientClass)










a = GeneralSearch('"حجاج العجمي"')
a.twitter_search()
a.google_search()

