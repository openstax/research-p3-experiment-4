from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from digital_logic.ext.markdown_ext import Markdown, markdown
from .accounts.models import User, Role
from .core import (db,
                   security,
                   mail,
                   webpack)
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

    if settings_override:
        app.config.from_object(settings_override)

    # register jinja2 extensions and filters
    jinja_extensions = [
        'jinja2.ext.do',
        'jinja2.ext.loopcontrols',
        'jinja2.ext.with_',
        Markdown
    ]

    app.jinja_options = app.jinja_options.copy()
    app.jinja_options['extensions'].extend(jinja_extensions)
    app.jinja_env.filters['markdown'] = markdown

    # Init extensions
    db.init_app(app)
    app.security = security.init_app(app,
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
