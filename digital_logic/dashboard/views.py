from flask import Blueprint, render_template
from flask_principal import Permission, RoleNeed
from flask_security import login_required

dashboard = Blueprint('home',
                      __name__,
                      template_folder='../templates/dashboard')

admin_permission = Permission(RoleNeed('admin'))


@dashboard.route('/')
@login_required
@admin_permission.require()
def index():
    return render_template('dashboard.html')
