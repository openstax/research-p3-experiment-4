from flask import Blueprint
from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .accounts.models import User, Role
from .core import api, db, security, mail, webpack
from .helpers import register_blueprints
from .redis_session import RedisSessionInterface

def create_app(package_name, package_path, settings_override=None):
    """
    This function creates the application using the application factory pattern.
    Extensions and blueprints are then initialized onto the the application
    object.

    http://flask.pocoo.org/docs/0.11/patterns/appfactories/

    :param package_name: the name of the package
    :param package_path: the path of the package
    :param settings_override: override default settings via a python object
    :return: app: the main flask application object
    """
    app = Flask(package_name,
                instance_relative_config=True,
                template_folder='templates')
    app.config.from_pyfile('config.py', silent=True)

    if settings_override is not None:
        app.config.from_object(settings_override)

    # Init extensions
    db.init_app(app)
    security.init_app(app,
                      SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=True)
    mail.init_app(app)
    webpack.init_app(app)

    # attach redis sessions
    app.session_interface = RedisSessionInterface(
        redis_host=app.config['REDIS_HOST'])

    # Helper function that registers all blueprints to the application
    register_blueprints(app, package_name, package_path)

    return app
