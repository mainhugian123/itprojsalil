from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/salil/flask/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), unique=True)
	username = db.Column(db.String(20), unique=True)
	email = db.Column(db.String())
	password = db.Column(db.String(80))

class LoginForm(Form):
	username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('Remember me')
class SignUpForm(Form):
	name = StringField('Name', validators=[InputRequired()])
	username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
	email = StringField('Email', validators=[InputRequired(), Email('Invalid email')])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return "Form Successfully Submitted"
	return render_template('login.html',form=form)
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		new_user = User(name = form.name.data,username = form.username.data, email = form.email.data, password = form.password.data)
		db.session.add(new_user)
		db.session.commit
		return "New User Has been created."
	return render_template('signup.html',form=form)
if __name__=='__main__':
	app.run(debug=True)