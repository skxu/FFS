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
  offset = request.args.get('offset')
  if form.validate_on_submit():
    new_query = ""

    if form.query.data:
      new_query+="query="+quote_plus(form.query.data)+"&"
    if form.min_field.data:
      new_query+="min="+quote_plus(str(form.min_field.data))+"&"
    if form.max_field.data:
      new_query+="max="+quote_plus(str(form.max_field.data))
    
    return redirect("market/browse?"+new_query)
  
  

  posts = []
  query = request.args.get('query')
  min_val = request.args.get('min')
  max_val = request.args.get('max')

  if query or min_val or max_val:
    print(query)
    query = None if not query else unquote(query)
    min_val = None if not min_val else unquote(min_val)
    max_val = None if not max_val else unquote(max_val)
    offset = 0 if not offset else offset
    posts = searchPost(query=query, min_val=min_val, max_val=max_val, offset=offset)
  else:
    posts = models.Post.query.filter_by(groupid=1).order_by(models.Post.update_date.desc()).offset(offset).limit(10).all()
    offset = 0 if not offset else offset
  return render_template("market/browse.html", user=g.user, posts=posts, form=form, offset=offset, query=query, min_val=min_val, max_val=max_val)

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = models.User.query.get(session['user_id'])

