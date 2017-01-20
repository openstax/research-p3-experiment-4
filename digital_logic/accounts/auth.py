from datetime import datetime

from flask import current_app as app, session
from flask_security import utils

from digital_logic.core import db
from digital_logic.experiment.business_logic import (
    get_subject_by_user_id,
    get_user_by_worker_id,
    get_experiment_group,
    create_subject)

from digital_logic.helpers import make_external_id


def create_user(email,
                password,
                active=False,
                registered_at=None,
                confirmed_at=None):
    user_datastore = app.extensions['security'].datastore
    password = utils.encrypt_password(password)

    user_obj = user_datastore.create_user(email=email,
                                          active=active,
                                          registered_at=registered_at,
                                          confirmed_at=confirmed_at,
                                          password=password)
    db.session.commit()

    return user_obj


def add_mturk_role_to_user(email):
    user_datastore = app.extensions['security'].datastore

    user_datastore.add_role_to_user(email, 'mturk')
    db.session.commit()

    return


def find_or_create_user(worker_id, assignment_id, hit_id):
    user = get_user_by_worker_id(worker_id)

    if not user:
        mturk_email = '{0}@mturk.com'.format(worker_id)
        password = worker_id
        active = True
        registered_at = datetime.now()
        confirmed_at = datetime.now()

        user = create_user(mturk_email,
                           password,
                           active,
                           registered_at,
                           confirmed_at)

    subject = get_subject_by_user_id(user.id)

    if not subject:
        data = dict()
        data['user_id'] = user.id
        data['worker_id'] = worker_id
        data['assignment_id'] = assignment_id
        data['hit_id'] = hit_id
        data['external_id'] = make_external_id(worker_id,
                                               assignment_id,
                                               hit_id)

        data['experiment_group'] = get_experiment_group(2)
        data['status'] = 'STARTED'

        subject = create_subject(data)

    return user, subject


def login_mturk_user(worker_id, assignment_id, hit_id):
    user, subject = find_or_create_user(worker_id, assignment_id, hit_id)
    assignment = get_latest_assignment(user_id)
    pass


def logout_mturk_user():
    utils.logout_user()


def _authenticate_mturk_worker(worker_id, assignment_id, hit_id):
    logout_mturk_user()
    session.clear()
    if worker_id and assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE':
        login_mturk_user(worker_id,
                         hit_id,
                         assignment_id)
