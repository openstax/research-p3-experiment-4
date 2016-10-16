import os

# Flask specific
SECRET_KEY = os.environ.get('SESSION_SECRET')
DEBUG = os.environ.get('FLASK_DEBUG')

# REDIS
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

# Flask-SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Flask-Mail
MAIL_PASSWORD = ''
MAIL_SERVER = ''
SLACK_WEBHOOK_URL = ''
MAIL_USERNAME = ''
MAIL_DEBUG = True

# Flask-Webpack
WEBPACK_MANIFEST_PATH = '../digital_logic/build/manifest.json'
# WEBPACK_ASSETS_URL = 'http://localhost:2992/static/'

# Flask-Security
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_SALT')
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = False
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'Openstax Labs<no-reply@labs.openstax.org>'
