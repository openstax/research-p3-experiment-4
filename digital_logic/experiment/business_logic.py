import random
from collections import Counter

from digital_logic.accounts.models import User
from digital_logic.core import db
from digital_logic.experiment.models import UserSubject as Subject


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

    subjects = db.session.query(Subject)\
        .filter(Subject.status == 'COMPLETED')\
        .all()

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

def get_latest_user_assignment(user_id):
    pass
