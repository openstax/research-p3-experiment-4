import psycopg2
import pytest

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from pytest_dbfixtures.factories.postgresql import init_postgresql_database, \
    drop_postgresql_database
from pytest_dbfixtures.utils import get_config
from webtest import TestApp

from digital_logic import create_app
from digital_logic.core import db as _db

from utils import populate_data


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
    settings = {
        'TESTING': True,
        'SECRET_KEY': 'a key for testing',
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': config_database,
        'WTF_CSRF_ENABLED': False,
        'SECURITY_REGISTERABLE': False,
        'WEBPACK_MANIFEST_PATH': '../digital_logic/build/manifest.json',
        'LOGIN_REQUIRED': False
    }

    # Ensure our migrations have been ran.
    # alembic.command.upgrade(config.alembic_config(), "head")
    config = AlembicConfig('alembic.ini')
    upgrade(config, 'head')

    return settings


@pytest.yield_fixture(scope='session')
def app(app_config):
    """An application for the tests."""
    _app = create_app()
    _app.config.update(app_config)

    ctx = _app.test_request_context()
    ctx.push()

    populate_data(_app.security.datastore)

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    """
    Configure a WebTest client for nice convenience methods."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app, request):
    """The database used for testing"""
    _db.app = app

    yield _db

    _db.session.close()
