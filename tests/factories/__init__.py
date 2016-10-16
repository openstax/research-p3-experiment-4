from factory import LazyAttribute, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from flask.ext.security.utils import encrypt_password

from digital_logic.core import db
from digital_logic.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):

    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = LazyAttribute(lambda a: encrypt_password('password'))
    active = True

    class Meta:
        """Factory configuration"""

        model = User
