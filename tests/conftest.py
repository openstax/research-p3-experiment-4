import psycopg2
import pytest
from pytest_dbfixtures.factories.postgresql import init_postgresql_database, \
    drop_postgresql_database
from pytest_dbfixtures.utils import get_config
from pytest_factoryboy import register
from webtest import TestApp

from digital_logic import create_app
from digital_logic.core import db
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
        'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://postgres@localhost:5432/tests',
        'WTF_CSRF_ENABLED': False,
        'SECURITY_REGISTERABLE': False,
        'WEBPACK_MANIFEST_PATH' : '../digital_logic/build/manifest.json'
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
def database(app, request):
    """The database used for testing"""
    db.app = app
    config = get_config(request)
    pg_host = config.postgresql.host
    pg_port = config.postgresql.port
    pg_user = config.postgresql.user
    pg_db = config.postgresql.db

    init_postgresql_database(psycopg2, pg_user, pg_host, pg_port, pg_db)

    with app.app_context():
        db.create_all()

    yield db

    db.session.close()

    drop_postgresql_database(psycopg2, pg_user, pg_host, pg_port, pg_db, '9.4')


@pytest.fixture(scope='function')
def user(database, user_factory):
    """A user for the tests"""
    _user = user_factory(password='iH3@r7P1zz@')
    database.session.commit()
    return _user
