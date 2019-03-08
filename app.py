from flask import Flask, redirect, render_template, request, session, abort, url_for, flash, redirect, session
from flaskext.mysql import MySQL
from forms import RegistrationForm, LoginForm, forgotPassForm, bankProfileForm, clientForm, oldCommentForm, newCommentForm, dbSetupForm,reportCase,ViewCasesForm
from DBconnection import connection2, BankConnection
from passwordRecovery import passwordRecovery
from datetime import datetime
import configparser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af6695d867da3c7d125a99f5c17ea79a'
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'SMIhmwn19*'
app.config['MYSQL_DATABASE_DB'] = 'SMI_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # Check id user exisit in the database
        cur, db = connection2()
        '''query = "SELECT * FROM AMLOfficer WHERE userName = '" + form.username.data + "' AND password = '" + form.password.data + "' "
        cur.execute(query)
        data1 = cur.fetchone()
        if data1 is None:
            flash('Invalid username or password please try again', 'danger')
            return render_template('login.html', form=form)
        else:
            query = "SELECT email FROM AMLOfficer WHERE userName = '" + form.username.data + "'"
            cur.execute(query)
            useremail = cur.fetchone()
            session["username"] = form.username.data
            session["email"] = useremail
            flash(f'Welcome back {form.username.data}', 'success')
            return redirect(url_for('bankP'))
        db.commit()
        cur.close()
        db.close()'''
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
            cur, db = connection2()
            query = "INSERT INTO AMLOfficer (userName, email, fullname, password, bank_id ) VALUES(%s,%s,%s,%s,%s)"
            val = (form.username.data, form.email.data, form.fullName.data, form.password.data, 1)
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
        cur, db = connection2()
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


@app.route("/bankProfile")
def bankP():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))

    return render_template("bankProfile.html")


@app.route("/ManageProfile", methods=['GET', 'POST'])
def manageProfile():
    form = bankProfileForm()
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        flash('Great','success')

    return render_template("ManageProfile.html", form = form)


@app.route("/ManageBankData")
def manageBankData():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))

    return render_template("ManageBankData.html")



@app.route("/clientProfile", methods=['GET', 'POST'])
def clientProfile():
    client_form = clientForm()
    new_comment = newCommentForm()
    old_comment = oldCommentForm()
    cur, db = connection2()
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    else:
        #Retrive client Info from database:
        query = "SELECT * FROM SMI_DB.Client WHERE clientID = 1"
        cur.execute(query)
        record = cur.fetchall()
        result=[]
        for column in record:
            client_form.clientID.data = column[0] #clientID
            client_form.clientName.data = column[1] #clientName
            client_form.clientSalary.data = column[2] #clientSalary
            client_form.clientClass.data = column[3]  #clientClass

    cur, db = connection2()
    query = "SELECT * FROM SMI_DB.Comment WHERE clientID = 1"
    cur.execute(query)
    record = cur.fetchall()
    if not (record is None) :
        for column in record:
            old_comment.PrecommentDate.data = column[2] #comment date
            old_comment.PrecommentContent.data = column[1] #comment body
        return render_template("clientProfile.html", clientForm=client_form, commentForm=new_comment,
                               oldCommentForm=old_comment)
    if new_comment.validate_on_submit():
        date_now = datetime.now()
        formatted_date = date_now.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO SMI_DB.Comment (commentBody, commentDate, clientID, officerName ) VALUES(%s,%s,%s,%s)"
        val = (new_comment.commentBody.data, formatted_date, formatted_date, 1, session['username'])
        cur.execute(query, val)
        db.commit()
        cur.close()
        db.close()

    return render_template("clientProfile.html", clientForm = client_form, commentForm = new_comment)


'''@app.route("/addComment")
def comment():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))'''

@app.route("/DatabaseSetup", methods=['GET', 'POST'])
def DatabaseSetup():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    form = dbSetupForm()
    if form.validate_on_submit():


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
            return render_template("databaseSetup.html", form=form)
        else:
            # Check if bussinse rule is uploaded
            flash('Successfully connected to the database..', 'success')
            return render_template("databaseSetup.html", form=form)





    return render_template("databaseSetup.html", form = form)

@app.route("/Report", methods=['GET', 'POST'])
def Report():
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    form = reportCase()
    if not(form.validate_on_submit()):
        return render_template("email.html", form=form)

        '''flash('Successfully connected to the database..', 'success')
        return render_template("databaseSetup.html", form=form)

    else:
        flash('Unable to connect please try again..', 'danger')'''



    return render_template("email.html", form = form)

@app.route("/Cases" , methods=['GET', 'POST'])
def cases():
    cur, db = connection2()
    # Only logged in users can access bank profile
    if session.get('username') == None:
        return redirect(url_for('home'))
    else:
        query = "SELECT * FROM SMI_DB.ClientCase "
        cur.execute(query)
        data = cur.fetchall()
        form = ViewCasesForm()
        if form.validate_on_submit():
            print(form.submit)
            id = request.form['submit'][-1]
            return redirect((url_for('case' , id = id)))
    return render_template("cases.html", data=data, form=form)








if __name__ == "__main__":
    app.run(debug=True)
