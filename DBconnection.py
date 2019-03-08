from flask import Flask, redirect, render_template, request, session, abort, url_for
from flaskext.mysql import MySQL
import mysql.connector
import configparser
from sqlalchemy import create_engine
import pyrebase



def connection():
    app = Flask(__name__)
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'SMIhmwn19*'
    app.config['MYSQL_DATABASE_DB'] = 'SMI_DB'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    mysql.init_app(app)

    conn = mysql.connect()
    cursor = conn.cursor()

    return cursor, conn

def connection2():

    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="SMIhmwn19*",
                                 db="SMI_DB",
                                 autocommit=True)
    cur = db.cursor()

    engine = create_engine("mysql+mysqlconnector://root:SMIhmwn19*@localhost/SMI_DB")

    return cur, db, engine


def BankConnection():

    status=0


    config = configparser.ConfigParser()
    config.read('credentials.ini')

    cur, db, engine = connection2()


    try:
        db = mysql.connector.connect(host=config['DB_credentials']['host'],
                                     user=config['DB_credentials']['user'],
                                     passwd=config['DB_credentials']['passwd'],
                                     db=config['DB_credentials']['db'])
        cur = db.cursor()

        engineParamter = 'mysql+mysqlconnector://' + config['DB_credentials']['user'] + ':' + config['DB_credentials']['passwd'] + '@' + config['DB_credentials']['host'] + '/' + config['DB_credentials']['db']
        engine = create_engine(engineParamter)

    except Exception as e:
        status =1
    return status, cur, db, engine








def firebaseConnection():
    config = {
        "apiKey": "AIzaSyBdvcfSBiaMQjb0q9g04emiCFYksGMvJfo",
        "authDomain": "saudi-money-investigator.firebaseapp.com",
        "databaseURL": "https://saudi-money-investigator.firebaseio.com",
        "projectId": "saudi-money-investigator",
        "storageBucket": "saudi-money-investigator.appspot.com",
        "messagingSenderId": "1098052350164"

    }

    return pyrebase.initialize_app(config)



