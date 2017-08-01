import datetime

from digital_logic.experiment.models import SubjectAssignment
from digital_logic.experiment.service import get_assignment, \
    all_subject_assignments, get_subject_by_user_id, get_user_by_worker_id, \
    create_subject_assignment, save_assignment_response


def test_get_assignment(db):
    assignment_id = 1
    assignment = get_assignment(assignment_id)
    assert assignment.mturk_assignment_id == 'debug45678'


def test_all_subject_assignments(db):
    subject_id = 2
    assignments = all_subject_assignments(subject_id)
    assert len(assignments) == 1


def test_get_subject_by_user_id(db):
    user_id = 3
    subject = get_subject_by_user_id(user_id)
    assert subject
    assert subject.mturk_worker_id.startswith('debug')


def test_get_user_by_worker_id(db):
    mturk_worker_id = 'debug5FQYY0'
    user = get_user_by_worker_id(mturk_worker_id)
    assert user


def test_create_subject_assignment(db):
    subject_id = 3
    assignment_phase = 'Assessment'
    assignment_id = 5
    hit_id = 'testhit'
    expire_time = 10
    assignment = create_subject_assignment(
        subject_id=subject_id,
        assignment_phase=assignment_phase,
        assignment_id=assignment_id,
        hit_id=hit_id,
        expire_time=expire_time,
        ua_dict={}
    )
    assert assignment


def test_save_assignment_response(db):
    assignment_id = 2
    exercise_id = 2
    credit = 1
    selection = 1
    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    end_time = None

    response = save_assignment_response(
        assignment_id=assignment_id,
        exercise_id=exercise_id,
        credit=credit,
        selection=selection,
        start_time=start_time,
        end_time=end_time
    )
    assert response
    assert response.assignment_id == assignment_id


