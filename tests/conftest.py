import os

import pytest
from pytest_factoryboy import register
from webtest import TestApp

from digital_logic.core import db

from digital_logic import create_app
from factories import UserFactory

# Use the pytest_factory_boy plugin and register the Model Factory
register(UserFactory)


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    settings = {
        'TESTING': True,
        'SECRET_KEY': 'a key for testing',
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://postgres@localhost:5433/test',
        'WTF_CSRF_ENABLED': False,
        'SECURITY_REGISTERABLE': False
    }

    _app = create_app()
    _app.config.update(settings)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def database(app):
    """The database used for testing"""
    # print(app.config)
    db.app = app
    with app.app_context():
        db.create_all()

    yield db

    db.session.close()
    db.drop_all()


@pytest.fixture(scope='function')
def user(database, user_factory):
    """A user for the tests"""
    _user = user_factory(password='iH3@r7P1zz@')
    database.session.commit()
    return _user
