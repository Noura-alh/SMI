from flask import Flask, redirect, render_template, request, session, abort, url_for
from flaskext.mysql import MySQL



def connection():
    app = Flask(__name__)
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'SMIhmwn19*'
    app.config['MYSQL_DATABASE_DB'] = 'SMI_DB'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    conn = mysql.connect()
    cursor = conn.cursor()

    return cursor, conn



