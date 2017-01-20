import random
from collections import Counter

from digital_logic.accounts.models import User
from digital_logic.core import db
from digital_logic.experiment.models import UserSubject as Subject, \
    SubjectAssignment, AssignmentResponse


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


def create_subject_assignment(subject_id, assignment_phase, assignment_id,
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
                assignment.id).delete()
