from datetime import datetime
import logging
import random
from collections import Counter

from flask import session
from flask_login import current_user
from sqlalchemy import and_
import numpy as np

from digital_logic.accounts.models import User
from digital_logic.alg.P3code.p3_selectquestion import prepare_question_params, \
    update
from digital_logic.core import db
from digital_logic.experiment.models import UserSubject as Subject, \
    SubjectAssignment, AssignmentResponse, AssignmentSession, Exercise, \
    UserSubject, SparfaTrace

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def all_subject_assignments(subject_id):
    return SubjectAssignment.get_all_by_subject_id(subject_id)


def get_subject_by_user_id(user_id):
    return Subject.get_by_user_id(user_id)


def get_user_by_worker_id(worker_id):
    return User.get_by_worker_id(worker_id)


def get_exercise(exercise_id):
    return Exercise.get(exercise_id)


def get_assignment(assignment_id):
    return SubjectAssignment.get(assignment_id)


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


def get_latest_subject_assignment(subject_id, assignment_phase=None):
    assignment = SubjectAssignment.get_lastest_by_subject_id(subject_id,
                                                             assignment_phase)
    return assignment


def create_subject_assignment(subject_id,
                              assignment_phase,
                              assignment_id,
                              hit_id,
                              ua_dict):
    assignment = SubjectAssignment(subject_id=subject_id,
                                   assignment_phase=assignment_phase,
                                   mturk_hit_id=hit_id,
                                   mturk_assignment_id=assignment_id,
                                   created_on=datetime.utcnow(),
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
    assessment_session = AssignmentSession.all_by_assignment_id(assignment.id)

    if responses:
        for response in responses:
            db.session.delete(response)
        db.session.commit()

    if assessment_session:
        for s in assessment_session:
            db.session.delete(s)
        db.session.commit()

    db.session.delete(assignment)
    db.session.commit()


def save_session_record(assignment_id, status):
    assignment_session = AssignmentSession(assignment_id=assignment_id,
                                           status=status,
                                           start_time=datetime.utcnow())
    db.session.add(assignment_session)
    db.session.commit()
    log.info(
        'Recording session status {0} for assignment {1}'.format(assignment_id,
                                                                 status))
    return assignment_session


def save_assignment_predictions(assignment_id, prediction_results):
    assignment = get_assignment(assignment_id)
    assignment.assignment_predictions = prediction_results
    db.session.add(assignment)
    db.session.commit()

    return


def list_answered_exercise_ids(subject_id, assignment_id):
    query = db.session.query(
        Exercise.id, Exercise.qb_id, Exercise.level).join(
        AssignmentResponse).join(
        SubjectAssignment).filter(
        SubjectAssignment.subject_id == subject_id,
        SubjectAssignment.id == assignment_id)

    return query.all()


def list_unanswered_exercise_ids(subject_id, assignment_id):
    subquery = db.session.query(AssignmentResponse).join(
        SubjectAssignment).filter(
        SubjectAssignment.subject_id == subject_id).subquery()
    return db.session.query(Exercise.id, Exercise.qb_id, Exercise.level).filter(
        and_(Exercise.level >= 0,
             ~Exercise.id.in_(subquery))).all()


def get_assignment(assignment_id):
    return SubjectAssignment.get(assignment_id)


def save_assignment_response(assignment_id,
                             exercise_id,
                             credit,
                             selection,
                             start_time,
                             end_time=None):
    ex_response = AssignmentResponse(assignment_id=assignment_id,
                                     exercise_id=exercise_id,
                                     credit=credit,
                                     selection=selection
                                     )
    assignment = get_assignment(assignment_id)

    # Check if the subject is in control or experimental group
    subject = get_subject_by_assignment_id(assignment_id)

    if (int(subject.experiment_group) == 1
        and exercise_id != 64 and assignment.assignment_phase == 'Practice'):
        training_set = db.session.query(SparfaTrace).first()
        # if subject is in experiment group update the
        # mastery matrix with the new response
        H = np.fromstring(training_set.H, dtype='float64').reshape((29, 4))
        d = np.fromstring(training_set.d, dtype='float64').reshape((4, 29))
        wmu = np.fromstring(training_set.wmu, dtype='float64').reshape((5, 29))
        Gamma = np.fromstring(training_set.Gamma, dtype=np.float64).reshape(
            (4, 4, 29))
        y = credit
        mastery = np.array(assignment.mastery, dtype=np.float64)
        K, Q = d.shape

        question_params_all = prepare_question_params(Q, H, d, wmu, Gamma)
        question_ids = np.fromstring(training_set.question_ids, dtype="<U7")

        # get the exercise to lookup the qb_id
        exercise = get_exercise(exercise_id)
        answered_index = np.where(question_ids == exercise.qb_id)
        answered_index = answered_index[0][0]
        mp, Vp = update(y, question_params_all[answered_index], mastery)
        k = np.where(H[answered_index,] > 0)[0][0]
        mastery[k] = mp
        mastery[K + k] = Vp
        assignment.mastery = mastery.tolist()
        db.session.add(assignment)

    ex_response.started_on = start_time
    end_time = end_time or datetime.utcnow()
    ex_response.completed_on = end_time
    response_time = (end_time - start_time).total_seconds()
    ex_response.user_response_time = response_time
    db.session.add(ex_response)

    db.session.commit()


def get_latest_assignment_by_user_id(user_id):
    return db.session.query(SubjectAssignment).join(Subject).filter(
        Subject.user_id == user_id).filter(
        SubjectAssignment.is_complete == True).order_by(
        SubjectAssignment.created_on.desc())


def get_subject_by_assignment_id(assignment_id):
    return db.session.query(UserSubject).join(SubjectAssignment).filter(
        SubjectAssignment.id == assignment_id).first()


def get_subject_assignment_response_by_qb_id(assignment_id, qb_id):
    return db.session.query(AssignmentResponse).join(Exercise).filter(
        Exercise.qb_id == qb_id).filter(
        AssignmentResponse.assignment_id == assignment_id).first()


def get_exercise_by_qb_id(qb_id):
    return Exercise.get_by_qb_id(qb_id)


def get_current_assignment_session():
    if current_user.is_authenticated:
        return db.session.query(AssignmentSession).filter(
            AssignmentSession.assignment_id == session[
                'current_assignment_id']).order_by(
            AssignmentSession.start_time.desc()).first()
    else:
        return None


def get_monkey_catcher_score(assignment_id):
    monkey = db.session.query(AssignmentResponse).filter(
        AssignmentResponse.assignment_id == assignment_id,
        AssignmentResponse.exercise_id == 64).first()
    if monkey:
        return monkey.credit
    else:
        return None


def qualify_assignment(assignment_id):
    # Get the data required to figure out total reading time.
    # When did they start reading? When Starting session was set.

    start_time = db.session.query(AssignmentSession.start_time).filter(
        AssignmentSession.assignment_id == assignment_id,
        AssignmentSession.status == 'Reading').first()

    end_time = db.session.query(AssignmentSession.start_time).filter(
        AssignmentSession.assignment_id == assignment_id,
        AssignmentSession.status == 'Finalizing'
    ).first()

    reading_time = (end_time[0] - start_time[0]).total_seconds()


    monkey_catcher_score = get_monkey_catcher_score(assignment_id)
    if reading_time >= 10 or monkey_catcher_score == 1:
        assignment = get_assignment(assignment_id)
        assignment.mturk_assignment_status = 'Accepted'
        assignment.mturk_assignment_status_date = datetime.utcnow()
        db.session.add(assignment)
        db.session.commit()
        return True
    else:
        return False
