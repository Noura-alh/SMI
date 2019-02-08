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




#@app.route("/")
#def index():
    #return render_template("index.html", title="RequestAccount")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Register")
def register():
    form = RegistrationForm()
    return render_template('Register.html', form =form)

@app.route("/TestRegister", methods=['GET', 'POST'])
def testRegister():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))

    return render_template('TestRegister.html', title ='Register', form = form)





@app.route("/User_register", methods=['GET', 'POST'])
def Registeratin():
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
      flash(f'Account created for {form.username.data}!', 'success')
      return redirect(url_for('home'))

  return render_template('Register.html', form=form)















@app.route("/login")
def login():
    return render_template("login.html")


#AMLOfficer Login

@app.route("/checkUser", methods=['GET', 'POST'])
def check():
    if  request.method == "POST":
        user_name = request.form['user']
        password = request.form['password']
        cursor.execute("SELECT * FROM AMLOfficer WHERE userName='"+user_name+"' and password= '"+password+"'")
        user = cursor.fetchone()
        cursor.close()

        if len(user) is 1:
            return redirect(url_for("bankP"))
        else:
            return "Failed"


@app.route("/bankP")
def bankP():
    return render_template("bankProfile.html")

if __name__ == "__main__":
    app.run(debug=True)






