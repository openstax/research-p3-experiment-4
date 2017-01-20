import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from pytest_postgresql.factories import (init_postgresql_database,
                                         drop_postgresql_database,
                                         get_config)
from webtest import TestApp

from digital_logic import create_app
from digital_logic.core import db as _db
from utils import populate_data, create_subjects, create_assignments


@pytest.yield_fixture(scope='session')
def config_database(request):
    connection_string = 'postgresql+psycopg2://{0}@{1}:{2}/{3}'

    config = get_config(request)
    pg_host = config.get('host')
    pg_port = config.get('port') or 5432
    pg_user = config.get('user')
    pg_db = config.get('db', 'tests')

    # Create the database
    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    yield connection_string.format(pg_user, pg_host, pg_port, pg_db)

    # Ensure the database gets deleted
    drop_postgresql_database(
        pg_user, pg_host, pg_port, pg_db, '9.4'
    )


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
    create_subjects(_db)
    create_assignments(_db)

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def test_client(app):
    """
    Configure a WebTest client for nice convenience methods."""
    return TestApp(app)


@pytest.yield_fixture(scope='session')
def db(app):
    """The database used for testing"""
    _db.app = app

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
