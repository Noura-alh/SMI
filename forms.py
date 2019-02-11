from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
   fullName = StringField('Full Name', validators=[DataRequired()])
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   bankName = StringField('Bank Name', validators=[DataRequired()])
   email = StringField('Email', validators= [DataRequired(), Email()])
   password = PasswordField('Password', validators= [DataRequired(), Length(min=8)])
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
   submit = SubmitField('Register')


class LoginForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   password = PasswordField('Password', validators= [DataRequired()])
   submit = SubmitField('Login')

class forgotPassForm(FlaskForm):
   email = StringField('Email', validators=[DataRequired(), Email()])
   submit = SubmitField('Send')


class bankProfileForm(FlaskForm):
   fullName = StringField('Full Name', validators=[DataRequired(), Length(min=2)])
   bankName = StringField('Bank Name', validators=[DataRequired()])
   email = StringField('AML Officer Email', validators=[DataRequired(), Email()])
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
   confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
   submit = SubmitField('Save Changes')
   delete = SubmitField('Delete Profile')
   cancel = SubmitField('Cancel')



class clientForm(FlaskForm):
   clientName = StringField('Client Name')
   clientClass = IntegerField('client class')
   clientID = IntegerField('Client ID')
   clientSalary = FloatField('Client Salary')


class oldCommentForm(FlaskForm):
   PrecommentDate = StringField('Date')
   PrecommentContent = StringField('Comment')
   delete = SubmitField('Delete')

class newCommentForm(FlaskForm):
   commentBody = TextAreaField('Add Comment', validators=[DataRequired()], render_kw={"rows": 5, "cols": 11})
   submit = SubmitField('Add Comment')


class dbSetupForm(FlaskForm):
   db_user = StringField('Database User: ', validators=[DataRequired()])
   db_pass = PasswordField('Database Password: ', validators= [DataRequired()])
   db_name = StringField('Database Name: ', validators=[DataRequired()])
   db_host = StringField('Database Host: ', validators=[DataRequired()])
   submit = SubmitField('Connect')






