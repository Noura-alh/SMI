from flask import Flask, redirect, render_template, request, session, abort, \
    url_for, flash, redirect, session, jsonify,Markup, render_template_string,make_response
from flaskext.mysql import MySQL
from flask_paginate import Pagination, get_page_parameter
from forms import RegistrationForm, LoginForm, forgotPassForm, bankProfileForm, \
    clientForm, oldCommentForm, newCommentForm, dbSetupForm,reportCase,ViewCasesForm,SearchForm,manageBankDataForm
from DBconnection import connection2, BankConnection,firebaseConnection
from passwordRecovery import passwordRecovery
from MachineLearningLayer.Detect import Detection
from datetime import datetime
import configparser
from celery import Celery, current_task
import random
import time
from flask_mail import Mail, Message
import os
from celery.result import AsyncResult
import json
import pdfkit


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['SECRET_KEY'] = 'af6695d867da3c7d125a99f5c17ea79a'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'SMIhmwn19*'
app.config['MYSQL_DATABASE_DB'] = 'SMI_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'smi.ksu2019@gmail.com'
app.config['MAIL_PASSWORD'] = 'SMIHMWN19'
app.config['MAIL_DEFAULT_SENDER'] = 'smi.ksu2019@gmail.com'


mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

# Initialize extensions
mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#Firebase connection

firebase = firebaseConnection()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test", methods=['GET', 'POST'])
def uplaoadfile():
    isuploaded = 0
    json_exttintion = 0

    target = os.path.join(APP_ROOT, 'Br_file/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files.get('file_br')
    print(file)
    if file is None:
        return render_template("file.html",isuploaded = 1, json_exttintion = json_exttintion )
    filename = file.filename
    print(filename)

    if filename.split(".", 1)[1] != 'json':
        json_exttintion = 1
        return render_template("file.html", isuploaded = isuploaded, json_exttintion=1)

    else:
        dest = "/".join([target, filename])
        print(dest)
        file.save(dest)
        ## make sure all variables in dataset ###






    return render_template("file.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # Check id user exisit in the database
        cur, db, enginec = connection2()
        cur.execute("SELECT COUNT(1) FROM AMLOfficer WHERE userName = %s;", [form.username.data])  # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM AMLOfficer WHERE userName = %s;", [form.username.data])  # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if form.password.data == row[0]:
                    session['username'] = form.username.data
                    query2 = "SELECT email FROM AMLOfficer WHERE userName = '" + form.username.data + "'"
                    cur.execute(query2)
                    useremail = cur.fetchone()
                    session["email"] = useremail
                    cur.execute("UPDATE SMI_DB.AMLOfficer SET numOfFailedLogin=%s WHERE userName='%s' " % (0, form.username.data)) #SUCCESSFUL LOGIN SET #ofTries to zero
                    db.commit()
                    flash(f'Welcome back {form.username.data}', 'success')
                    return redirect(url_for('bankP'))


                else:
                    cur.execute("SELECT numOfFailedLogin FROM AMLOfficer WHERE userName = %s;",[form.username.data])  # FETCH THE HASHED PASSWORD
                    for row in cur.fetchall():
                        if row[0]== 3:
                            flash('Sorry You have entered your password 3 times wrong.. Enter your email for validation to reset your password', 'danger')
                            return redirect(url_for('forgotPass'))



                        else:
                            cur.execute("UPDATE SMI_DB.AMLOfficer SET numOfFailedLogin= numOfFailedLogin+1 WHERE userName='%s' " % (form.username.data))  # SUCCESSFUL LOGIN SET #ofTries to zero
                            db.commit()
                            flash('Wrong Password try again!', 'danger')

        else:
            flash('Invalid Username try again!', 'danger')
            db.commit()
            cur.close()
            db.close()
    #task = long_task.apply_async()
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # remove the username and email from the session if it is there
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route("/Register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Checking If the account(user_name) is already registered.
        cursor.execute("SELECT * FROM AMLOfficer WHERE userName = '" + form.username.data + "'")
        data1 = cursor.fetchone()

        # Checking If the account(email) is already registered.
        cursor.execute("SELECT * FROM AMLOfficer WHERE email = '" + form.email.data + "'")
        data2 = cursor.fetchone()
        if not (data1 is None):
            flash('This Username is already registered please try another username', 'danger')
            return render_template('Register.html', form=form)
        elif not (data2 is None):
            flash('This Email is already registered please try another email', 'danger')
            return render_template('Register.html', form=form)
        else:
            cur, db, engine = connection2()
            query = "INSERT INTO AMLOfficer (userName, email, fullname, password ) VALUES(%s,%s,%s,%s)"
            val = (form.username.data, form.email.data, form.fullName.data, form.password.data)
            cur.execute(query, val)
            db.commit()
            cur.close()
            db.close()
            session["username"] = form.username.data
            session['email'] = form.email.data
            flash(f'Account created for {session["username"]} Successfully !', 'success')
        return redirect(url_for('bankP'))

    return render_template('Register.html', form=form)


@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPass():
    form = forgotPassForm()
    if form.validate_on_submit():
        # Check id user exisit in the database
        cur, db, engine = connection2()
        query = "SELECT * FROM SMI_DB.AMLOfficer WHERE email ='" + form.email.data + "'"
        cur.execute(query)
        data1 = cur.fetchone()
        if (data1 is None):
            flash('This email is not registered in our system ', 'danger')
            return render_template('forgotPassword.html', form=form)
        else:
            a = passwordRecovery(form.email.data)
            a.sendEmail()

            flash('A recovery password has been sent to your email', 'success')
            return render_template('forgotPassword.html', form=form)

    return render_template("forgotPassword.html", form=form)


@app.route("/bankProfile" , methods=['GET', 'POST'])
def bankP():
    if session.get('username') == None:
        return redirect(url_for('home'))
    cur, db, engine = connection2()
    query = "SELECT * FROM SMI_DB.ClientCase WHERE viewed ='1'"
    cur.execute(query)
    totalAlert = cur.fetchall()
    totalAlert = len(totalAlert)
    print(totalAlert)
    form = SearchForm()
    if form.validate_on_submit():
        return redirect((url_for('searchResult', id= form.search.data)))  # or what you want
    return render_template("bankProfile.html", form = form, alert = totalAlert)


@app.route("/ManageProfile", methods=['GET', 'POST'])
def manageProfile():
    form = bankProfileForm()
    search_form = SearchForm()
    username = session.get('username')
    if session.get('username') == None:
        return redirect(url_for('home'))

    if form.profile_submit.data and form.validate_on_submit():
        cur, db , engine = connection2()
        cur.execute("UPDATE SMI_DB.AMLOfficer SET fullname = '" + form.fullName.data + "' , email = '" + form.email.data + "' , userName = '" + form.username.data + "', password = '" + form.password.data + "' WHERE userName = '" + username + "'" )
        db.commit()

    if search_form.search_submit.data and search_form.validate_on_submit():
        return redirect((url_for('searchResult', id= search_form.search.data , form2 = search_form )))

    return render_template("ManageProfile.html", form=form , form2 = search_form )


@app.route("/ManageBankData", methods=['GET', 'POST'])
def manageBankData():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    form = manageBankDataForm()
    search_form = SearchForm()
    status, cur, db, engine = BankConnection()
    file_submit = 0
    file_exttintion =0
    isFB_Connected = 'false'
    if form.bank_submit.data and form.validate_on_submit():
        ## check if there's prevoius BR and confirm to update it

        print()
        target = os.path.join(APP_ROOT, 'Br_file/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)

        file = request.files.get('file_br')
        print(file)
        if file is None:
            return render_template("ManageBankData.html", form=form, form2=search_form, isFB_Connected=isFB_Connected, file_submit =1)
        filename = file.filename
        print(filename)

        if filename.split(".", 1)[1] != 'txt':
            file_exttintion = 1
            return render_template("ManageBankData.html", form=form, form2=search_form, isFB_Connected=isFB_Connected, file_submit=file_submit, file_exttintion = 1 )

        else:
            dest = "/".join([target, filename])
            print(dest)
            file.save(dest)
        try:
            db = firebase.database()
            isFB_Connected = db.child('Rule3').child('suspiciousTransaction').child('amount').get().val()
            # businessRules_file = businessRules_file.data
            sanction_list = open("Br_file/" + filename, "r")
            risk_countries = form.risk_countries.data
            exceed_avg_tran = form.exceed_avg_tran.data
            # type1 = form.type.data
            amount = form.amount.data
            db.child('Rule1').child('highRiskCountries').set(risk_countries)
            db.child('Rule2').child('exceedingAvgTransaction').set(exceed_avg_tran)
            # db.child('Rule3').child('suspiciousTransaction').child('Type').set(type1)
            db.child('Rule3').child('suspiciousTransaction').child('amount').set(amount)
            db.child('Rule4').child('blackList').set(sanction_list.read().splitlines())
        except Exception as e:
            flash('Please connect to the Internet..', 'danger')
            return render_template("databaseSetup.html", form=form, status=status)


        if status == 1: # If upload BR and didn't set DB redirect to database setup
            flash('Successfully uploaded your business rules..Setup your database connection to start the analysis', 'success')
            form = dbSetupForm()
            return render_template("databaseSetup.html", form=form, status= status)

        if status == 0:
            task = Analysis.delay()
            form2 = SearchForm()
            flash('Successfully uploaded your business rules..', 'success')
            return render_template('analysisView.html', JOBID=task.id, form2=form2)

        return redirect((url_for('manageBankData', form=form, form2=search_form, isFB_Connected = isFB_Connected, file_submit=file_submit)))

    if search_form.search_submit.data and search_form.validate_on_submit():
        return redirect((url_for('searchResult', id=search_form.search.data, form2=search_form)))


    return render_template("ManageBankData.html", form=form, form2=search_form, isFB_Connected = isFB_Connected, file_submit=file_submit)


@app.route("/clientProfile/<id>", methods=['GET', 'POST'])
def clientProfile(id):
    client_form = clientForm()
    new_comment = newCommentForm()
    old_comment = oldCommentForm()
    cur, db, engine = connection2()

    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    else:
        # Retrive client Info from database:
        query = "SELECT * FROM SMI_DB.Client WHERE clientID = '" + id + "'"
        cur.execute(query)
        record = cur.fetchall()
        result = []
        for column in record:
            client_form.clientID.data = column[0]  # clientID
            client_form.clientName.data = column[1]  # clientName
            client_form.clientSalary.data = column[2]  # clientSalary
            client_form.clientClass.data = column[3]  # clientClass

        cur, db, engine = connection2()
        query = "SELECT * FROM SMI_DB.Comment WHERE clientID = '" + id + "'"
        cur.execute(query)
        record = cur.fetchall()

        # if not (record is None) :
        # for column in record:
        # old_comment.PrecommentDate.data = column[2] #comment date
        # old_comment.PrecommentContent.data = column[1] #comment body
        # return render_template("clientProfile.html", clientForm=client_form, commentForm=new_comment,oldCommentForm=old_comment)

        if new_comment.add_submit.data and new_comment.validate_on_submit():
            print("works")
            cur, db, engine = connection2()
            date_now = datetime.now()
            formatted_date = date_now.strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO SMI_DB.Comment (commentBody, commentDate, clientID, officerName ) VALUES(%s,%s,%s,%s)"
            val = (new_comment.commentBody.data, formatted_date, id, session['username'])
            print(new_comment.commentBody.data)
            cur.execute(query, val)
            db.commit()
            cur.close()
            db.close()
            return redirect(url_for('clientProfile', commentForm=new_comment, id=id))

        print(old_comment.delete.data)

        if old_comment.validate_on_submit():
            print('the delete works')
            cur, db, engine = connection2()
            id1 = request.form['Delete_comment']
            print(id)
            print(id1)
            query = "DELETE FROM SMI_DB.Comment WHERE commentID = '" + id1 + "'"
            cur.execute(query)
            return redirect(url_for('clientProfile', oldCommentForm=old_comment, id1=id1, id=id))


        return render_template("clientProfile.html", clientForm=client_form, commentForm=new_comment, record=record,oldCommentForm=old_comment)


@app.route("/DatabaseSetup", methods=['GET', 'POST'])
def DatabaseSetup():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    form = dbSetupForm()
    status, cur, db, engine = BankConnection()
    try:
     db = firebase.database()
     isFB_Connected = db.child('Rule3').child('suspiciousTransaction').child('amount').get().val()
    except Exception as e:
        flash('Please connect to the Internet..', 'danger')
        return render_template("databaseSetup.html", form=form, status=status)




    if form.validate_on_submit():
        if status == 0: # If the user tried to connect to already connected DB
            config = configparser.ConfigParser()
            config.read('credentials.ini')

            if form.db_host.data==config['DB_credentials']['host']\
                    and form.db_name.data == config['DB_credentials']['db']\
                    and form.db_pass.data == config['DB_credentials']['passwd']\
                    and form.db_user.data == config['DB_credentials']['user']:

                flash('You are already connected to this database..', 'success')
                return render_template("databaseSetup.html", form=form, status = status)

        config = configparser.ConfigParser()
        config['DB_credentials'] = {'host': form.db_host.data,
                                    'user': form.db_user.data,
                                    'passwd': form.db_pass.data,
                                     'db': form.db_name.data}
        with open('credentials.ini', 'w') as configfile:
            config.write(configfile)
        status, cur, db, engine= BankConnection()
        if status == 1:
            flash('Unable to connect please try again..', 'danger')
            return render_template("databaseSetup.html", form=form, status = status)
        else:
            if isFB_Connected == 'false':
                flash('Successfully connected to the database..Upload your business rules to start the analysis', 'success')
                search_form = SearchForm()
                form = manageBankDataForm()
                return render_template("ManageBankData.html", form=form, form2=search_form)
            else:
                task = Analysis.delay()
                form2 = SearchForm()
                flash('Successfully connected to the database..', 'success')
                return render_template('analysisView.html', JOBID=task.id, form2=form2)

                # Check if bussinse rule is uploaded
            flash('Successfully connected to the database..', 'success')
            return render_template("databaseSetup.html", form=form, status = status)
    if status == 0:  # If DB is already set bring the form.
        config = configparser.ConfigParser()
        config.read('credentials.ini')
        form.db_host.data = config['DB_credentials']['host']
        form.db_name.data = config['DB_credentials']['db']
        form.db_pass.data = config['DB_credentials']['passwd']
        form.db_user.data = config['DB_credentials']['user']


    return render_template("databaseSetup.html", form = form, status = status)

@app.route("/Report/<id>", methods=['GET', 'POST'])
def Report(id):
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    form = reportCase()
    cur, db, engine = connection2()
    cur.execute("SELECT * FROM SMI_DB.ClientCase WHERE caseID=%s " % (id))
    record = cur.fetchall()
    client_ID = record[0][3]
    caseNumber = ''
    caseDate = ''

    for each1 in record:
        caseNumber = each1[0]
        caseDate = each1[2]

    profileLabel = ''
    if record[0][1] == 'Low':  # Need to change it Meduim
        profileLabel = 'label label-warning'
    else:  # High
        profileLabel = 'label label-danger'
    label_name = record[0][1]

    # --------------------#----------------------#--------------------------#-------------#

    query1 = "SELECT * FROM SMI_DB.SuspiciousTransaction WHERE clientID=%s " % (client_ID)
    cur.execute(query1)
    record1 = cur.fetchall()
    transaction_number = ''
    transaction_type = ''
    transaction_amount = ''
    transaction_location = ''
    old_balance = ''
    new_balance = ''

    for each in record1:
        transaction_number = each[15]
        transaction_type = each[1]
        transaction_amount = each[2]
        transaction_location = each[13]
        old_balance = each[7]
        new_balance = each[8]

    query2 = "SELECT * FROM SMI_DB.Client WHERE clientID=%s " % (client_ID)
    cur.execute(query2)
    record2 = cur.fetchall()
    clientName = ''
    for each in record2:
        clientName = each[1]

    rendered = render_template('CaseToPrint.html', clientName=clientName, caseNumber=caseNumber, caseDate=caseDate,
                               label=profileLabel, label_name=label_name, transaction_number=transaction_number,
                               transaction_type=transaction_type, transaction_amount=transaction_amount,
                               transaction_location=transaction_location,
                               old_balance=old_balance, new_balance=new_balance)
    #######save case to working dierctory ##########
    pdfFile = pdfkit.from_string(rendered, 'case.pdf')
    #request.files.get('file_case') = pdfFile
    #request.form['file_case'] = pdfFile
    form.subject.data = 'Case#{}_{}'.format(id,clientName)
    form.email_body.data = 'Fruad Report'

    if form.validate_on_submit():
        '''target = os.path.join(APP_ROOT, 'Case_file/')
        print('target',target)
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files.get('file_case')
        print('file',file)
        filename = file.filename
        print('fileNAME',filename)
        dest = "/".join([target, filename])
        print(dest)
        file.save(dest)'''
        recipient = form.reciver.data
        msg = Message(form.subject.data, recipient.split())
        msg.body = form.email_body.data
        with app.open_resource("case.pdf") as fp:
            msg.attach("case.pdf", "case/pdf", fp.read())
        print(msg)
        mail.send(msg)

        flash('Email has been sent Successfully..', 'success')
    return render_template("email.html", form = form, clientID= id)

@app.route("/Cases" , methods=['GET', 'POST'])
def cases():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    else:
        cur, db, engine = connection2()
        form = ViewCasesForm()
        search_form = SearchForm()
        per_page = 4
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * per_page
        query = "SELECT * FROM SMI_DB.ClientCase "
        cur.execute(query)
        total = cur.fetchall()
        countCases = len(total)
        cur.execute("SELECT * FROM SMI_DB.ClientCase ORDER BY caseID DESC LIMIT %s OFFSET %s", (per_page, offset))
        cases = cur.fetchall()

        if search_form.search_submit.data and search_form.validate_on_submit():
            return redirect((url_for('searchResult', id=search_form.search.data, form2=search_form)))

        if form.validate_on_submit():
            # id = form.hidden.data
            # id = request.form.get('case_submit')
            id = request.form['caseView']
            # id2 = request.form['caseDownload']
            print(id)
            return redirect((url_for('case', id=id)))

        pagination = Pagination(page=page, per_page=per_page, total=len(total), offset=offset, search=search,
                                record_name='cases', css_framework='bootstrap3')

        return render_template("cases.html", cases=cases, form=form, form2=search_form, pagination=pagination,css_framework='foundation', caseId=0, countCases=countCases)

@app.route("/case/<id>", methods=['GET', 'POST'])
def case(id):
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    search_form = SearchForm()

    if search_form.search_submit.data and search_form.validate_on_submit():
        return redirect((url_for('searchResult', id=search_form.search.data, form2=search_form)))


    cur, db, engine = connection2()
    cur.execute("SELECT * FROM SMI_DB.ClientCase WHERE caseID=%s " % (id))
    data = cur.fetchall()
    client_ID = data[0][3]
    profileLabel=''
    if data[0][1] == 'Medium':#Need to change it Meduim
        profileLabel ='label label-warning'
    else:#High
        profileLabel = 'label label-danger'

    cur.execute("SELECT * FROM SMI_DB.Client WHERE clientID=%s " % ( client_ID))
    data2 = cur.fetchall()
    client_BR = data2[0][5]
    Br_flag = True
    print('Br', client_BR)
    Br_dic = {}
    if client_BR == '0000':
        Br_flag = False
    else:
        if client_BR[0] == '1':
            Br_dic['1'] = 'Client Name is in sanction list'
        if client_BR[1] == '1':
            Br_dic['2'] = 'Client location in risk contries'
        if client_BR[2] == '1':
            Br_dic['3'] = 'Client exceeded avg amount of transactions'
        if client_BR[3] == '1':
            Br_dic['4'] = 'Client exceeded max amount of transaction'

    cur.execute("SELECT * FROM SuspiciousTransaction WHERE clientID=%s " % (client_ID))
    transaction = cur.fetchall()

    return render_template("case.html",data= data, data2= data2, label= profileLabel, clientId = id, transaction=transaction, Br_flag=Br_flag ,Br_dic=Br_dic)

@app.route("/caseTOprint/<id>", methods=['GET', 'POST'])
def caseTOprint(id):
    # Only logged in users can access bank profile

    if session.get('username') == None:
        return redirect(url_for('home'))
    search_form = SearchForm()



    cur, db, engine = connection2()
    cur.execute("SELECT * FROM SMI_DB.ClientCase WHERE caseID=%s " % (id))
    data = cur.fetchall()
    client_ID = data[0][3]
    profileLabel=''
    if data[0][1] == 'Low':#Need to change it Meduim
        profileLabel ='label label-warning'
    else:#High
        profileLabel = 'label label-danger'

    cur.execute("SELECT * FROM SMI_DB.Client WHERE clientID=%s " % ( client_ID))
    data2 = cur.fetchall()

    cur.execute("SELECT * FROM SuspiciousTransaction WHERE clientID=%s " % (client_ID))
    transaction = cur.fetchall()

    return render_template("caseTOprint.html",data= data, data2= data2, label= profileLabel, clientId = id, transaction=transaction)


@app.route('/download/<id>', methods=['GET','POST'])
def download(id):
    cur, db, engine = connection2()
    query = "SELECT * FROM SMI_DB.ClientCase WHERE caseID = '" + id + "'"
    cur.execute(query)
    record = cur.fetchall()
    client_ID = record[0][3]
    caseNumber = ''
    caseDate = ''

    for each1 in record:
        caseNumber = each1[0]
        caseDate = each1[2]

    profileLabel = ''
    if record[0][1] == 'Low':  # Need to change it Meduim
        profileLabel = 'label label-warning'
    else:  # High
        profileLabel = 'label label-danger'
    label_name = record[0][1]

    # --------------------#----------------------#--------------------------#-------------#

    query1 = "SELECT * FROM SMI_DB.SuspiciousTransaction WHERE clientID=%s " % (client_ID)
    cur.execute(query1)
    record1 = cur.fetchall()
    transaction_number = ''
    transaction_type = ''
    transaction_amount = ''
    transaction_location = ''
    old_balance = ''
    new_balance = ''

    for each in record1:
        transaction_number = each[15]
        transaction_type = each[1]
        transaction_amount = each[2]
        transaction_location = each[13]
        old_balance = each[7]
        new_balance = each[8]

    query2 = "SELECT * FROM SMI_DB.Client WHERE clientID=%s " % (client_ID)
    cur.execute(query2)
    record2 = cur.fetchall()
    clientName = ''
    for each in record2:
        clientName = each[1]

    rendered = render_template('CaseToPrint.html', clientName=clientName, caseNumber=caseNumber, caseDate=caseDate,
                               label=profileLabel, label_name=label_name, transaction_number=transaction_number,
                               transaction_type=transaction_type, transaction_amount=transaction_amount,
                               transaction_location=transaction_location,
                               old_balance=old_balance, new_balance=new_balance)

    pdf = pdfkit.from_string(rendered, False)
    #######save case to working dierctory ##########
    #pdfkit.from_string(rendered, 'case.pdf')

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=case.pdf'
    return response


######CELERY PART #########

@app.route('/startAnalysis')
def startAnalysis():
    return render_template_string('''<a href="{{ url_for('enqueue') }}">start</a>''')

@app.route('/enqueue')
def enqueue():
    task = Analysis.delay()
    form2 = SearchForm()
    return render_template('analysisView.html', JOBID=task.id, form2=form2)

@app.route('/analysisView')
def analysisView():
    form2 =SearchForm()
    return render_template("analysisView.html",form2= form2)

@app.route('/progress')
def progress():
    jobid = request.values.get('jobid')
    if jobid:
        # GOTCHA: if you don't pass app=celery here,
        # you get "NotImplementedError: No result backend configured"
        job = AsyncResult(jobid, app=celery)
        print (job.state)
        print (job.result)
        if job.state == 'PROGRESS':
            return json.dumps(dict(
                state=job.state,
                progress=job.result['current']*1.0/job.result['total'],
            ))
        elif job.state == 'SUCCESS':
            return json.dumps(dict(
                state=job.state,
                progress=1.0,
            ))
    return '{}'

@celery.task
def Analysis():
    d = Detection()
    d.Detect()


if __name__ == "__main__":
    app.run(debug=True)
