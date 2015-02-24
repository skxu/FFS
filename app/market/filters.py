from app import app
from datetime import date, datetime

#old format: 2015-02-24 06:45:53.000000
#new format 2015-02-24
def format_date(s):
	time = datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
	return time.strftime("%b-%d-%Y %I:%M %p")
	
	
app.jinja_env.filters['formatdate'] = format_date