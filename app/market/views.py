from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.market.forms import SearchForm
import app.users.models as models
from app.users.decorators import requires_login
from app.models.post import searchPost
from urllib import quote_plus
from urllib2 import unquote
from flask.ext import wtf

mod = Blueprint('market', __name__, url_prefix='/market')

@mod.route('/browse/', methods=["GET","POST"])
@mod.route('/browse', methods=["GET","POST"])
@mod.route('/browse.html', methods=["GET","POST"])
def home():
  form = SearchForm(request.form)

  if form.validate_on_submit():
    new_query = quote_plus(form.query.data)
    
    return redirect("market/browse?query="+new_query)
  else:
    print(request.method)
  

  posts = []
  query = request.args.get('query')
  if query:
    print(query)
    query = unquote(query)
    posts = searchPost(query)
  else:
    posts = models.Post.query.filter_by(groupid=1).order_by(models.Post.update_date.desc()).limit(10).all()
  return render_template("market/browse.html", user=g.user, posts=posts, form=form)

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = models.User.query.get(session['user_id'])

