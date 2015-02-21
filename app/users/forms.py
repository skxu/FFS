from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
	email = TextField('Email address', [Required(), Email()])
	password = PasswordField('Password', [Required()])

class RegisterForm(Form):
	username = TextField('Username', [Required()])
	email = TextField('Email address', [Required(), Email()])
	password = PasswordField('Password', [Required()])
	confirm = PasswordField('Repeat Password', [
		Required(),
		EqualTo('password', message='Passwords must match')
		])
	accept_tos = BooleanField('I accept the TOS', [Required()])

