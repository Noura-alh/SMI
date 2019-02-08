from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
   fullName = StringField('Full Name', validators=[DataRequired()])
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', validators= [DataRequired(), Email()])
   password = PasswordField('Password', validators= [DataRequired()])
   confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
   submit = SubmitField('Register')


class LoginForm(FlaskForm):
   ''' username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])'''

   #email = StringField('Email', validators=[DataRequired(), Email()])
   username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', validators= [DataRequired(), Email()])
   password = PasswordField('Password', validators= [DataRequired()])
   submit = SubmitField('Login')

