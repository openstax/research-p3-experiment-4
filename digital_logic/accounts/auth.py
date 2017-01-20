import logging
from datetime import datetime

from flask import current_app as app, session
from flask_principal import Permission, RoleNeed
from flask_security import utils

from digital_logic.core import db
from digital_logic.experiment.service import (
    create_subject,
    get_subject_by_user_id,
    get_user_by_worker_id,
    get_experiment_group,
    get_latest_subject_assignment, create_subject_assignment,
    purge_subject_assignment_data)
from digital_logic.helpers import make_external_id

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

mturk_permission = Permission(RoleNeed('mturk'))


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


def create_mturk_role():
    user_datastore = app.extensions['security'].datastore
    user_datastore.find_or_create_role(name='mturk',
                                       description='Mechanical Turk User')
    db.session.commit()


def add_mturk_role_to_user(email):
    user_datastore = app.extensions['security'].datastore
    create_mturk_role()

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
        data['mturk_worker_id'] = worker_id
        data['external_id'] = make_external_id(worker_id,
                                               assignment_id,
                                               hit_id)

        data['experiment_group'] = get_experiment_group(2)

        subject = create_subject(data)

    return user, subject


def login_mturk_user(worker_id, assignment_id, hit_id):
    user, subject = find_or_create_user(worker_id, assignment_id, hit_id)

    add_mturk_role_to_user(user.email)

    success = utils.login_user(user, False)

    if success:
        log.info(
            'user {0} with worker_id {1} has been logged in successfully'.format(
                user.id, subject.mturk_worker_id))
        return user, subject
    else:
        raise Exception('Subject could not be logged into the system')


def logout_mturk_user():
    session.clear()
    utils.logout_user()


def _login_and_prep_subject(worker_id,
                            assignment_id,
                            hit_id,
                            ua_dict,
                            debug_mode=False):
    if worker_id and assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE':
        user, subject = login_mturk_user(worker_id,
                                         hit_id,
                                         assignment_id)

        latest_assignment = get_latest_subject_assignment(subject.id)
        assignment_phases = app.config['ASSIGNMENT_PHASES']

        if latest_assignment and debug_mode:
            purge_subject_assignment_data(latest_assignment.id)
            latest_assignment = None

        if not latest_assignment:
            assignment = create_subject_assignment(subject.id,
                                                   assignment_phases[0],
                                                   assignment_id,
                                                   hit_id,
                                                   ua_dict)
            return assignment
        elif latest_assignment.assignment_phase == assignment_phases[0]:
            subject_user = get_subject_by_user_id(user.id)
            if subject_user and latest_assignment.mturk_hit_id != hit_id:
                assignment = create_subject_assignment(subject.id,
                                                       assignment_phases[1],
                                                       assignment_id,
                                                       hit_id,
                                                       ua_dict)
                return assignment
