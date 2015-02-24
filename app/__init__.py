import os
import sys
import logging
from logging.handlers import SMTPHandler

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask("FFS", template_folder=tmpl_dir)

#setup configurations
app.config.from_object('config')

#setup mailing error logs
#mail_handler = SMTPHandler('127.0.0.1', 'ffs_error@code.io', app.config['ADMINS'], 'APPLICATION FAILURE')
#mail_handler.setLevel(logging.ERROR)
#app.logger.addHandler(mail_handler)

#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG


#setup file logging

###NON-WINDOWS CONFIG###
file_handler = logging.FileHandler("ffs.log")

###WINDOWS CONFIG###
#file_handler = logging.handlers.NTEventLogHandler("ffs")

file_handler.setLevel(logging.DEBUG)

from logging import Formatter
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)
app.logger.debug(app.config)

db = SQLAlchemy(app)
Bootstrap(app)

import cron



@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

from app.users.views import mod as usersModule
from app.market.views import mod as marketModule
app.register_blueprint(usersModule)
app.register_blueprint(marketModule)

from app.market import filters

#TODO create API & make separate webapp