from flask.ext.wtf import Form
from wtforms import TextField, DecimalField
from wtforms.validators import Optional, NumberRange

class SearchForm(Form):
	query = TextField('Search')

	min_field = DecimalField('Minimum', [Optional(), NumberRange(min=0)])
	max_field = DecimalField("Maximum", [Optional(), NumberRange(min=0)])

