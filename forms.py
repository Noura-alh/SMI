from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, FileField, SelectMultipleField
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

class reportCase(FlaskForm):
   reciver = StringField('To: ', validators= [DataRequired(), Email()])
   subject = StringField('Sujbect: ', validators=[DataRequired()])
   email_body = TextAreaField('Message: ', render_kw={"rows": 5, "cols": 11},validators=[DataRequired()])
   #case_report = FileField('Upload Business Rules:1')
   submit = SubmitField('Send')
   #Report file:


class ViewCasesForm(FlaskForm):
   submit = SubmitField('View Case')


class SearchForm(FlaskForm):
   search = StringField('')
   search_submit = SubmitField('Search')


class ViewProfileForm(FlaskForm):
   view_submit = SubmitField('View Profile')

#Manage bank data from
class manageBankDataForm(FlaskForm):
   businessRules_file = FileField('Upload Business Rules:')
   sanction_list = FileField('Upload Sanction List:')
   risk_countries = SelectMultipleField('High Risk Countries:', choices=[('Afghanistan', 'Afghanistan') , ('Åland Islands', 'Åland Islands') ,
    ('Albania', 'Albania'), ('Algeria', 'Algeria') , ('American', 'American') , ('Andorra', 'Andorra') , ('Angola', 'Angola') , ('Anguilla', 'Anguilla')
     , ('Antarctica', 'Antarctica') , ('Antigua and Barbuda', 'Antigua and Barbuda') , ('Argentina', 'Argentina') , ('Armenia', 'Armenia')
      , ('Austria', 'Austria') , ('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh')
      , ('Barbados', 'Barbados'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'), ('Belize', 'Belize'),
      ('Benin', 'Benin'), ('Bermuda', 'Bermuda'), ('Bhutan', 'Bhutan'),
      ('Bolivia, Plurinational State of', 'Bolivia, Plurinational State of'),
      ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
      ('Botswana', 'Botswana'), ('Bouvet Island', 'Bouvet Island'), ('Brazil', 'Brazil'),
      ('British Indian Ocean Territory', 'British Indian Ocean Territory'), ('Brunei Darussalam', 'Brunei Darussalam'), ('Bulgaria', 'Bulgaria'),
      ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'), ('Cambodia', 'Cambodia'),
      ('Cameroon', 'Cameroon'), ('Canada', 'Canada'), ('Cape Verde', 'Cape Verde'), ('Cayman Islands', 'Cayman Islands'),
      ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'), ('Chile', 'Chile'), ('China', 'China'),
      ('Christmas Island', 'Christmas Island'), ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'), ('Colombia', 'Colombia'),
      ('Comoros', 'Comoros'), ('Congo', 'Congo'), ('Congo, the Democratic Republic of the', 'Congo, the Democratic Republic of the'),
      ('Cook Islands', 'Cook Islands'), ('Costa Rica', 'Costa Rica'), ('Côte d Ivoire', 'Côte d Ivoire'), ('Croatia', 'Croatia'),
      ('Cuba', 'Cuba') , ('Curaçao', 'Curaçao') , ('Cyprus', 'Cyprus') , ('Czech Republic', 'Czech Republic') , ('Denmark', 'Denmark') , ('Djibouti', 'Djibouti')
      , ('Dominica', 'Dominica') , ('Dominican Republic', 'Dominican Republic') , ('Ecuador', 'Ecuador') , ('Egypt', 'Egypt') , ('El Salvador', 'El Salvador') , ('Equatorial Guinea', 'Equatorial Guinea')
      , ('Eritrea', 'Eritrea'), ('Estonia', 'Estonia'), ('Ethiopia', 'Ethiopia'), ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'), ('Faroe Islands', 'Faroe Islands'),
      ('Fiji', 'Fiji'), ('Finland', 'Finland'), ('France', 'France'), ('French Guiana', 'French Guiana'), ('French Polynesia', 'French Polynesia'), ('French Southern Territories', 'French Southern Territories'),
      ('Gabon', 'Gabon'), ('Gambia', 'Gambia'), ('Georgia', 'Georgia'), ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greece', 'Greece'), ('Greenland', 'Greenland'), ('Grenada', 'Grenada'),
      ('Guadeloupe', 'Guadeloupe'), ('Guam', 'Guam'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'),
      ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'), ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'),
      ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran', 'Iran'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'),
      ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey') , ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Kiribati', 'Kiribati'), ('North Korea', 'North Korea'), ('South Korea', 'South Korea'),
      ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ('Lao', 'Lao'), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'), ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Liechtenstein', 'Liechtenstein'),
      ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Macao', 'Macao'), ('Macedonia', 'Macedonia'), ('Madagascar', 'Madagascar'), ('Malawi', 'Malawi'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'),
      ('Mali', 'Mali'), ('Malta', 'Malta'), ('Marshall Islands', 'Marshall Islands'), ('Martinique', 'Martinique'), ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'), ('Mayotte', 'Mayotte'),
      ('Mexico', 'Mexico'), ('Micronesia', 'Micronesia'), ('Moldova', 'Moldova'), ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Montserrat', 'Montserrat') , ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique')
      , ('Myanmar', 'Myanmar'), ('Namibia', 'Namibia'), ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Netherlands', 'Netherlands'), ('New Caledonia', 'New Caledonia'), ('New Zealand', 'New Zealand')
      , ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Niue', 'Niue'), ('Norfolk Island', 'Norfolk Island'), ('Northern Mariana Islands', 'Northern Mariana Islands')
      , ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'), ('Palestinian', 'Palestinian'), ('Panama', 'Panama'), ('Papua New Guinea', 'Papua New Guinea'), ('Paraguay', 'Paraguay'), ('Peru', 'Peru'), ('Philippines', 'Philippines'),
      ('Pitcairn', 'Pitcairn'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Puerto Rico', 'Puerto Rico'), ('Qatar', 'Qatar'), ('Réunion', 'Réunion'), ('Romania', 'Romania'), ('Russian', 'Russian'), ('Rwanda', 'Rwanda'),
      ('Saint Barthélemy', 'Saint Barthélemy'), ('Saint Helena', 'Saint Helena'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'), ('Saint Lucia', 'Saint Lucia'), ('Saint Martin', 'Saint Martin'),
      ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'), ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'), ('Samoa', 'Samoa'), ('San Marino', 'San Marino'), ('Sao Tome and Principe', 'Sao Tome and Principe'),
      ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Singapore', 'Singapore'), ('Sint Maarten', 'Sint Maarten'), ('Slovakia', 'Slovakia'),
      ('Slovenia', 'Slovenia'), ('Solomon Islands', 'Solomon Islands'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa') , ('South Georgia', 'South Georgia'), ('South Sudan', 'South Sudan'), ('Spain', 'Spain')
      , ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'), ('Suriname', 'Suriname'), ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'), ('Swaziland', 'Swaziland'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Syrian', 'Syrian') , ('Taiwan', 'Taiwan')
      , ('Tajikistan', 'Tajikistan'), ('Tanzania', 'Tanzania'), ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'), ('Tonga', 'Tonga'), ('Trinidad and Tobago', 'Trinidad and Tobago'),
      ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'), ('Turkmenistan', 'Turkmenistan'), ('Turks and Caicos Islands', 'Turks and Caicos Islands'), ('Tuvalu', 'Tuvalu'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('United Arab Emirates', 'United Arab Emirates'),
      ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'), ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan') , ('Vanuatu', 'Vanuatu'), ('Venezuela', 'Venezuela')
      , ('Viet Nam', 'Viet Nam'), ('Virgin Islands, British', 'Virgin Islands, British'), ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'), ('Wallis and Futuna', 'Wallis and Futuna'), ('Western Sahara', 'Western Sahara') , ('Yemen', 'Yemen'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe')])
   exceed_avg_tran = IntegerField('Exceeding Average Transactions With:' , validators=[DataRequired()] )
   #type = SelectField('Type: ' , choices=[('Transfer', 'Transfer') , ('Cash out', 'Cash out')])
   amount = IntegerField('Transaction Risk Amount:' , validators=[DataRequired()])
   bank_submit = SubmitField('submit')








