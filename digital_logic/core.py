from flask_restplus import Api
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_webpack import Webpack

api = Api(version='1.0', title='Digital Logic Exp 4 API',
          description='The digital logic web API')

db = SQLAlchemy()

mail = Mail()

security = Security()

webpack = Webpack()
