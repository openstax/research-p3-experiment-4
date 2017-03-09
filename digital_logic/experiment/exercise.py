import random

import numpy as np
from flask import current_app as app

from ..alg.P3code.p3_selectquestion import prepare_question_params, \
    question_selector
from digital_logic.core import db
from digital_logic.experiment.models import UserSubject, Exercise, \
    SubjectAssignment, SparfaTrace
from digital_logic.experiment.service import list_answered_exercise_ids, \
    list_unanswered_exercise_ids, get_subject_assignment_response_by_qb_id, \
    get_exercise_by_qb_id

Q_POOL = [1, 2, 9, 16, 17, 18, 19, 21, 22, 27,
          32, 34, 43, 44, 45, 48, 49, 50,
          51, 52, 53, 57, 58, 59, 60, 61, 62]

BEGINNER_POOL = [1, 9, 16, 18, 27, 32, 44, 48, 49, 50, 52, 58, 60, 61, 62]

INTERMEDIATE_POOL = [2, 17, 19, 21, 22, 34, 43, 45, 51, 53, 57, 59]

A_POOL = [4, 5, 11, 25, 31, 39, 40, 54, 56, 63]

STATIC_POOL = [42, 37, 55]

DEFAULT_E_NUM = 14

MONKEY_CATCHER = 64

MONKEY_INDEX = int(DEFAULT_E_NUM / 2)


def get_question_params():
    data = np.load('P3next.npy', encoding='latin1')
    H = data[0]
    d = data[1]
    wmu = data[2]
    Gamma = data[3]
    question_ids = data[4]

    K, Q = d.shape

    # re-format the trained info
    question_params_all = []
    for ii in range(Q):
        temp_question = []
        k = np.where(H[ii,] > 0)[0][0]
        temp_question = [wmu[k, ii], wmu[-1, ii], d[k, ii], Gamma[k, k, ii], k]
        question_params_all.append(temp_question)
    return question_params_all


def initialize_subject_exercises(subject_id, assignment_id):
    subject = UserSubject.get(subject_id)
    assignment = SubjectAssignment.get(assignment_id)

    assignment_phases = app.config['ASSIGNMENT_PHASES']

    # If they are in the Assesment phase load up the assessment pool questions
    if assignment.assignment_phase == assignment_phases[1]:
        assignment.exercise_pool = A_POOL
        db.session.add(assignment)
        db.session.commit()
    else:
        # If they are in the Experiment phase make a random equal distribution
        # of each level of question to make up for the number of items in the
        # assessment.
        # TODO: Make a random equal distribution of questions based on level
        if int(subject.experiment_group) == 0:

            answered_exercises = list_answered_exercise_ids(subject_id,
                                                            assignment_id)

            total_exercises = DEFAULT_E_NUM
            # static_pool = STATIC_POOL

            needed_exercises = total_exercises - len(answered_exercises) - 1

            # assessment_qs = A_POOL

            # unanswered = list_unanswered_exercise_ids(subject_id, assignment_id)
            # unanswered = [q_id for q_id in unanswered]

            beginner_pool = [q_id for q_id in BEGINNER_POOL if
                             q_id not in answered_exercises]

            intermediate_pool = [q_id for q_id in INTERMEDIATE_POOL if
                                 q_id not in answered_exercises]

            beginner_pool = random.sample(beginner_pool, 6)

            intermediate_pool = random.sample(intermediate_pool, 7)

            exercises = beginner_pool + intermediate_pool

            monkey_catcher = MONKEY_CATCHER
            monkey_catcher_index = int(needed_exercises / 2)

            exercises.insert(monkey_catcher_index, monkey_catcher)

            assignment.exercise_pool = exercises

            db.session.add(assignment)
            db.session.commit()
        else:
            assignment.exercise_pool = [STATIC_POOL[0]]
            assignment.mastery = [0, 0, 0, 0, 3, 3, 3, 3]
            db.session.add(subject)
            db.session.commit()


def get_subject_assessment_next_exercise(subject_id, assignment_id):
    subject = UserSubject.get(subject_id)
    assignment = SubjectAssignment.get(assignment_id)

    answered_exercises = list_answered_exercise_ids(subject.id, assignment.id)

    total_answered = len(answered_exercises)

    if total_answered < len(assignment.exercise_pool):
        exercise_id = assignment.exercise_pool[total_answered]
        exercise = Exercise.get(exercise_id)
        return exercise
    else:
        return None


def get_subject_next_exercise(subject_id, assignment_id):
    subject = UserSubject.get(subject_id)
    assignment = SubjectAssignment.get(assignment_id)

    answered_exercises = list_answered_exercise_ids(subject.id,
                                                    assignment.id)
    total_answered = len(answered_exercises)

    if subject.experiment_group == 0:

        if total_answered < DEFAULT_E_NUM:
            if total_answered == MONKEY_INDEX:
                exercise = Exercise.get(MONKEY_CATCHER)
                return exercise
            exercise_id = assignment.exercise_pool[total_answered]
            exercise = Exercise.get(exercise_id)
            return exercise
        else:
            return None
    else:
        if total_answered == MONKEY_INDEX:
            exercise = Exercise.get(MONKEY_CATCHER)
            return exercise

        elif total_answered < len(assignment.exercise_pool):
            exercise_id = assignment.exercise_pool[total_answered]
            exercise = Exercise.get(exercise_id)
            return exercise

        elif total_answered >= len(
                assignment.exercise_pool) and total_answered < DEFAULT_E_NUM:
            # TODO: Move this to its file somewhere!
            training_set = db.session.query(SparfaTrace).first()
            H = np.fromstring(training_set.H, dtype='float64').reshape((29, 4))
            d = np.fromstring(training_set.d, dtype='float64').reshape((4, 29))
            wmu = np.fromstring(training_set.wmu, dtype='float64').reshape(
                (5, 29))
            Gamma = np.fromstring(training_set.Gamma, dtype=np.float64).reshape(
                (4, 4, 29))
            mastery = np.array(assignment.mastery, dtype=np.float64)
            K, Q = d.shape

            qb_ids = np.fromstring(training_set.question_ids, dtype="<U7")

            # create an array of ones and zeroes to deterimene if the the question is
            # available to sparfa trace
            avail = []
            for qb_id in qb_ids:
                answered = get_subject_assignment_response_by_qb_id(
                    assignment.id,
                    qb_id)
                if answered:
                    avail.append(float(0.0))
                else:
                    avail.append(float(1.0))
            avail = np.array(avail)
            question_params_all = prepare_question_params(Q, H, d, wmu, Gamma)
            q = question_selector(question_params_all, avail, mastery, 1)[0]
            qb_id = qb_ids[q]
            return get_exercise_by_qb_id(qb_id)
        else:
            return None
