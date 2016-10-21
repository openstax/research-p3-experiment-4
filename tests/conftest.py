import psycopg2
import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from pytest_dbfixtures.factories.postgresql import init_postgresql_database, \
    drop_postgresql_database
from pytest_dbfixtures.utils import get_config
from pytest_factoryboy import register
from webtest import TestApp

from digital_logic import create_app
from digital_logic.core import db as _db
from factories import UserFactory

# Use the pytest_factory_boy plugin and register the Model Factory
register(UserFactory)


@pytest.fixture(scope='session')
def config_database(request):
    connection_string = 'postgresql+psycopg2://{0}@{1}:{2}/{3}'

    config = get_config(request)
    pg_host = config.postgresql.host
    pg_port = config.postgresql.port
    pg_user = config.postgresql.user
    pg_db = config.postgresql.db

    # Create the database
    init_postgresql_database(psycopg2, pg_user, pg_host, pg_port, pg_db)

    # Ensure the database gets deleted
    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(
            psycopg2, pg_user, pg_host, pg_port, pg_db, '9.4'
        )

    return connection_string.format(pg_user, pg_host, pg_port, pg_db)


@pytest.fixture(scope='session')
def app_config(config_database):
    print('Loading config')
    settings = {
        'TESTING': True,
        'SECRET_KEY': 'a key for testing',
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': config_database,
        'WTF_CSRF_ENABLED': False,
        'SECURITY_REGISTERABLE': False,
        'WEBPACK_MANIFEST_PATH': '../digital_logic/build/manifest.json'
    }

    # Ensure our migrations have been ran.
    # alembic.command.upgrade(config.alembic_config(), "head")
    config = AlembicConfig('alembic.ini')
    upgrade(config, 'head')

    return settings


@pytest.yield_fixture(scope='function')
def app(app_config):
    """An application for the tests."""

    _app = create_app()
    _app.config.update(app_config)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app, request):
    """The database used for testing"""
    _db.app = app

    yield _db

    _db.session.close()


@pytest.fixture(scope='function')
def user(db, user_factory):
    """A user for the tests"""
    _user = user_factory(password='iH3@r7P1zz@')
    db.session.commit()
    return _user
