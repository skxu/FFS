from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.users.forms import RegisterForm, LoginForm
import app.users.models as models
from app.users.decorators import requires_login

mod = Blueprint('market', __name__, url_prefix='/market')

@mod.route('/browse/')
def home():
  posts = []
  posts = models.Post.query.filter_by(groupid=1).order_by("update_date").limit(10).all()

  return render_template("market/browse.html", user=g.user, posts=posts)

@mod.before_request
def before_request():
  """
  pull user's profile from the database before every request are treated
  """
  g.user = None
  if 'user_id' in session:
    g.user = models.User.query.get(session['user_id'])

