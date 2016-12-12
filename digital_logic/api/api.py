import logging
import traceback

from flask import Blueprint, current_app
from sqlalchemy.orm.exc import NoResultFound

from digital_logic.exceptions import SectionNotFound
from .endpoints.ping import ns as ping_namespace
from .endpoints.exercises import ns as exercise_namespace
from .endpoints.subjects import ns as subjects_namespace
from .endpoints.textbook import ns as textbook_namespace
from ..core import api

log = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api/v1')

api.init_app(bp)

# Add namespaces
api.add_namespace(ping_namespace)
api.add_namespace(subjects_namespace)
api.add_namespace(textbook_namespace)
api.add_namespace(exercise_namespace)


# register error handlers
@api.errorhandler
def default_error_handler(e):  # pragma: no cover
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['FLASK_DEBUG']:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required '
                       'but none was found.'}, 404


@api.errorhandler(SectionNotFound)
def no_section_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'No section found for that part of the textbook'}, 404
