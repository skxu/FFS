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

FB_API_VERSION = 2.2

FB_APP_ID = '1458079401079497'
FB_APP_SECRET = '2ee36cdaf4f45f4aa35f954e5c790e9f'
FB_APP_NAME = 'FFS'
ACCESS_TOKEN = 'CAAUuHZADBcskBANkOCIjGAZBU3GsjS6STZBUPuIhDjBkEZC8BtnZBCw6ZCOKWjeP5snZBmOYtXzjmIOeBHwYajpaskQUY0rapia93KRNc05dHB1fKqiZBVGGfxrZAn5fXaVhnPPeqBnAnuHDsRbC6lt17NYmVz1YR2oneUignGU3D4VUrYlqHlJasOv5s12y6YdlcYnsnSYU6Kj52dSP2wcE9'


#temp for official facebook groups
BERKELEY_ID = '266259930135554'
NORTHWESTERN_ID = '357858834261047'

GROUP_ID_LIST = [BERKELEY_ID, NORTHWESTERN_ID]
