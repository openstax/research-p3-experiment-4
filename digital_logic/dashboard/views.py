from flask import Blueprint, render_template
from flask_security import login_required

dashboard = Blueprint('home',
                      __name__,
                      template_folder='../templates/dashboard')


@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard.html')
