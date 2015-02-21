import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask("FFS", template_folder=tmpl_dir)

#setup configurations
app.config.from_object('config')
print(app.config)


db = SQLAlchemy(app)

import cron


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

from app.users.views import mod as usersModule
app.register_blueprint(usersModule)