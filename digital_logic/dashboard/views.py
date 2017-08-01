from flask import Blueprint, render_template, request
from flask_principal import Permission, RoleNeed
from flask_security import login_required

from digital_logic.exceptions import ExperimentError

dashboard = Blueprint('home',
                      __name__,
                      template_folder='../templates/dashboard')

admin_permission = Permission(RoleNeed('admin'))


@dashboard.errorhandler(ExperimentError)
def error_handler(exception):
    return exception.error_page(request)


@dashboard.errorhandler(404)
def error_handler():
    exception = ExperimentError('page_not_found')
    return exception.error_page(request)


@dashboard.route('/')
@login_required
@admin_permission.require()
def index():
    return render_template('dashboard.html')
