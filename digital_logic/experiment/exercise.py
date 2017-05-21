import random

import numpy as np
from flask import current_app as app, session

from digital_logic.core import db
from ..alg.P3code.p3_selectquestion import (
    prepare_question_params,
    question_selector)

from .models import (
    Exercise,
    SparfaTrace)
from .service import (
    get_subject_assignment_response_by_qb_id,
    get_exercise_by_qb_id)
from ._constants import (BEGINNER_POOL,
                         INTERMEDIATE_POOL,
                         A_POOL,
                         DEFAULT_E_NUM,
                         MONKEY_CATCHER,
                         MONKEY_INDEX)


def get_question_params():  # pragma: no cover
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


def initialize_assignment_exercises(assignment):
    assignment_phases = app.config['ASSIGNMENT_PHASES']

    if assignment.assignment_phase == assignment_phases[1]:
        random.shuffle(A_POOL)
        assignment.exercise_pool = A_POOL
        db.session.add(assignment)
        db.session.commit()
    else:
        if int(assignment.subject.experiment_group) == 0:
            answered_exercises = [ex.id for ex in assignment.responses]
            total_exercises = DEFAULT_E_NUM
            needed_exercises = total_exercises - len(answered_exercises) - 1

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
            assignment.mastery = [0, 0, 0, 0, 3, 3, 3, 3]
            db.session.add(assignment)
            db.session.commit()


def next_exercise_from_pool(assignment):
    exercise_id = assignment.exercise_pool[assignment.total_answered]
    exercise = Exercise.get(exercise_id)

    return exercise


def get_available_exercises(assignment_id, qb_ids):
    """
    This function exists because of the importance of the reading sections and
    the way this algorithm selects exercises. Initially, we pooled from the
    set of exercises, however, the reading is split into two sections with a 
    period in between for practice exercises. The exercises for each
    part of the practice are generated with this algorithm.
    
    The qb_ids is an array we have taken from the train_set data that is loaded
    in the `get_next_exercise_from_algorithm` function. This represents all the
    exercises in the trained model. The qb_ids are used to create an array of 
    available exercises. If the exercise is not in the reading section pool or
    it has been answered it is set to 0.0 for unavailable.
    
    :param assignment_id: 
    :param qb_ids: all the qb_ids used by the trained model 
    :return avail: all the available exercises
    """

    exercises = Exercise.all()
    section = session['current_section']
    exercise_ids = section['exercises']

    non_pool_exercise_qb_ids = [exercise.qb_id for exercise in exercises if
                                exercise.id not in exercise_ids]
    pool_exercise_qb_ids = [exercise.qb_id for exercise in exercises if
                             exercise.id in exercise_ids]

    avail = []

    for qb_id in qb_ids:

        answered = get_subject_assignment_response_by_qb_id(
            assignment_id,
            qb_id
        )

        if answered or qb_id in non_pool_exercise_qb_ids:
            avail.append(float(0.0))
        elif qb_id in pool_exercise_qb_ids:
            avail.append(float(1.0))

    return avail


def get_next_exercise_from_algorithm(assignment):
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

    avail = get_available_exercises(assignment.id, qb_ids)

    question_params_all = prepare_question_params(Q, H, d, wmu, Gamma)
    q = question_selector(question_params_all, avail, mastery, 1)[0]
    qb_id = qb_ids[q]

    return qb_id


def experiment_group_next_exercise(assignment):
    if assignment.total_answered == MONKEY_INDEX:
        return Exercise.get(MONKEY_CATCHER)
    if assignment.total_answered < DEFAULT_E_NUM:
        qb_id = get_next_exercise_from_algorithm(assignment)
        return get_exercise_by_qb_id(qb_id)


def get_assignment_next_exercise(assignment):
    if assignment.assignment_phase == 'Practice':
        if int(assignment.subject.experiment_group) == 0:
            return next_exercise_from_pool(assignment)
        elif int(assignment.subject.experiment_group) == 1:
            return experiment_group_next_exercise(assignment)
    else:
        return next_exercise_from_pool(assignment)
