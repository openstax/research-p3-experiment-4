from . import factory
from .utils import make_database_url

def create_app(settings_override=None):
    return factory.create_app(__name__,
                              __path__,
                              settings_override)
