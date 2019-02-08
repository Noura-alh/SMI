from flask import Flask, redirect, render_template, request, session, abort, url_for, flash, redirect, session
from flaskext.mysql import MySQL
from forms import RegistrationForm , LoginForm
from DBconnection import connection2



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
        if form.username.data == 'admin' and form.password.data == 'password':
            flash(f'Welcome back {form.username.data}', 'success')
            return redirect(url_for('bankP'))
        else:
            flash('Login Unsuccessful, Please check username and password','danger')

    return render_template('login.html', form=form)

'''
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))
'''





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
          session["email"] = form.email.data
          flash(f'Account created for {session["username"]} Successfully !', 'success')
      return redirect(url_for('bankP')), session["username"],session["email"]

  return render_template('Register.html', form=form)







@app.route("/bankProfile")
def bankP():

    return render_template("bankProfile.html")

@app.route("/ManageProfile")
def manageProfile():
    return render_template("ManageProfile.html")


@app.route("/test")
def translate():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)






