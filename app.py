from flask import Flask, redirect, render_template, request, session, abort, url_for, flash, redirect
from flaskext.mysql import MySQL
from forms import RegistrationForm , LoginForm



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
cursor1 = conn.cursor()




@app.route("/")
def home():
    return render_template("home.html")



@app.route("/TestRegister", methods=['GET', 'POST'])
def testRegister():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))

    return render_template('TestRegister.html', title ='Register', form = form)





@app.route("/Register", methods=['GET', 'POST'])
def register():
  ''' fullName = request.form['name']
    userName = request.form['username']
    #bankName = request.form['bankName']
    email = request.form['email']
    confirmEmail = request.form['confirmEmail']
    password = request.form['password']
    confirmPass = request.form['confirmPassword']

    #Checking If the account(user_name) is already registered.
    cursor.execute("SELECT * FROM AMLOfficer WHERE userName = '"+userName+"'")
    data = cursor.fetchone()

    if not(data is None):
        return render_template('Register.html', error='This Username is already registered')

    # Checking If the account(email) is already registered.
    cursor.execute("SELECT * FROM AMLOfficer WHERE email = '" + email + "'")
    data = cursor.fetchone()

    if not (data is None):
        return 'This Email is already registered'

    return 'Working'   '''
  form = RegistrationForm()
  if form.validate_on_submit():
      flash(f'Account created for {form.username.data} Successfully !', 'success')
      return redirect(url_for('bankP'))

  return render_template('new.html', form=form)




'''@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)'''


#AMLOfficer Login

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash(f'You have been logged in!!', 'success')
            return redirect(url_for('bankP'))
        else:
            flash('Login Unsuccessful, Please check username and password','danger')

    return render_template('login.html', form=form)


@app.route("/bankProfile")
def bankP():
    return render_template("bankProfile.html")

@app.route("/ManageProfile")
def manageProfile():
    return render_template("ManageProfile.html")

if __name__ == "__main__":
    app.run(debug=True)






