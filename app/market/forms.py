from flask.ext.wtf import Form
from wtforms import TextField

class SearchForm(Form):
	query = TextField('Search')

