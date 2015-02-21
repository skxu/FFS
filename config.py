import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['skx@berkeley.edu'])
SECRET_KEY = '//ad8&dfd/sanAtiaLKNweuBG5'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = '*&sNJde8Hss7s7A&seglq['

API_VERSION = 2.2

FB_APP_ID = '1458079401079497'
FB_APP_SECRET = '2ee36cdaf4f45f4aa35f954e5c790e9f'
FB_APP_NAME = 'FFS'
ACCESS_TOKEN = 'CAAUuHZADBcskBAJB3S2EVIqwYSqk8zDFNVZB9jQX7ppEzFreWdZCuAK6zniTdIwk9cXLObuTjYRLYvg8ZCJv0sXBcNOzMoFkJSJp9n7ywksCakzyfH0psjnCo4h4V4mL8n4XZCdfZAcN2s8fvCZCTdRMXge1dR4de1B3hCziDTC4E2GZBZB0nBurXgVttpspRYMwfvLGLsBFbORWXw5I5QVTo'

