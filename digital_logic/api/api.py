from flask import Blueprint
from ..core import api

from .endpoints.ping import ns as ping_namespace

bp = Blueprint('api', __name__, url_prefix='/api/v1')

api.init_app(bp)

api.add_namespace(ping_namespace)
