from flask import Flask, redirect, render_template, request, session, abort, url_for
from flaskext.mysql import MySQL
import mysql.connector



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
                                 db="SMI_DB")
    cur = db.cursor()

    return cur, db


def BankConnection(host_name,user_name,password,db_name):

    status=0
    cur = ""
    db = ""
    try:
        db = mysql.connector.connect(host=host_name,
                                     user=user_name,
                                     passwd=password,
                                     db=db_name)
        cur = db.cursor()

    except Exception as e:
        status =1


    return status, cur , db



