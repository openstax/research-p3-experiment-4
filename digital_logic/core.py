from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_webpack import Webpack
from digital_logic.mturk import MTurk


db = SQLAlchemy()

mail = Mail()

security = Security()

webpack = Webpack()

mturk = MTurk()
