from flask import Flask, redirect, render_template, request, session, abort, url_for
from flaskext.mysql import MySQL
from DBconnection import connection
import requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
import pprint


class webScraping:

    def __init__(self, clientName):
        self.clientName = clientName
        self.url = 'https://www.google.co.in/search?q={}'.format(self.clientName)
        self.document = ''
        self.textDocument = ''
        self.cleanText = ''
        self.keyWords = {}

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
        SearchClass = 0
        clientClass = ''
        for keys, values in self.keyWords.items():
            if values > 0 :
                sum_of_frequencies += values
                numOfApearance += 1
        try:
            #max(100)*size*apearance

            SearchClass = (sum_of_frequencies / (numOfApearance * 21 ))
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
        print('Frequeancy', sum_of_frequencies)
        print('SearchClass Weight', SearchClass)
        print('Client Class', clientClass)










a = webScraping('اختلاس غش')
a.run()
