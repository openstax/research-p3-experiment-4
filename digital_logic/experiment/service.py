import logging
import random
from collections import Counter

from digital_logic.accounts.models import User
from digital_logic.core import db
from digital_logic.experiment.models import UserSubject as Subject, \
    SubjectAssignment, AssignmentResponse, AssignmentSession

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def all_subject_assignments(subject_id):
    return SubjectAssignment.get_all_by_subject_id(subject_id)


def get_subject_by_user_id(user_id):
    return Subject.get_by_user_id(user_id)


def get_user_by_worker_id(worker_id):
    return User.get_by_worker_id(worker_id)


def get_experiment_group(num_groups):
    """
    This will take a number of conditions and counter-balance the number of
    subjects in each condition.
    :param num_groups: (int) number of groups
    :return: group
    """
    counts = Counter()

    subjects = db.session.query(Subject).join(SubjectAssignment).filter(
        SubjectAssignment.is_complete == True).all()

    for cond in range(num_groups):
        counts[cond] = 0

    for subject in subjects:
        counts[subject.experiment_group] += 1

    min_count = min(counts.values())

    minimums = [hash for hash, count in counts.items() if count == min_count]

    return random.choice(minimums)


def create_subject(data):
    subject = Subject(**data)
    db.session.add(subject)
    db.session.commit()

    return subject


def update_subject(subject_id, data):
    subject = Subject.get(subject_id)

    for k, v in data.items():
        setattr(subject, k, v)

    db.session.add(subject)
    db.session.commit()

    return subject


def get_latest_subject_assignment(subject_id):
    assignment = SubjectAssignment.get_lastest_by_subject_id(subject_id)
    return assignment


def create_subject_assignment(subject_id,
                              assignment_phase,
                              assignment_id,
                              hit_id, ua_dict):
    assignment = SubjectAssignment(subject_id=subject_id,
                                   assignment_phase=assignment_phase,
                                   mturk_hit_id=hit_id,
                                   mturk_assignment_id=assignment_id,
                                   **ua_dict)
    db.session.add(assignment)
    db.session.commit()

    return assignment


def purge_subject_data(subject_id):
    subject_assignments = SubjectAssignment.get_all_by_subject_id(subject_id)

    if subject_assignments:
        for assignment in subject_assignments:
            responses = AssignmentResponse.all_by_assignment_id(
                assignment.id)
            if responses:
                responses.delete()
                db.session.add(responses)
            db.session.delete(assignment)
            db.session.add(assignment)
    db.session.commit()


def purge_subject_assignment_data(assignment_id):
    assignment = SubjectAssignment.get(assignment_id)
    responses = AssignmentResponse.all_by_assignment_id(assignment.id)
    sessions = AssignmentSession.all_by_assignment_id(assignment.id)

    if responses:
        for response in responses:
            db.session.delete(response)
        db.session.commit()

    if sessions:
        for session in sessions:
            db.session.delete(session)
        db.session.commit()

    db.session.delete(assignment)
    db.session.commit()


def add_session_record(assignment_id, status):
    assignment_session = AssignmentSession(assignment_id=assignment_id,
                                status=status)
    db.session.add(assignment_session)
    db.session.commit()
    log.info(
        'Recording session status {0} for assignment {1}'.format(assignment_id,
                                                                 status))
    return assignment_session
