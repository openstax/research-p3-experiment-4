from random import random

from flask import current_app as app

from digital_logic.core import db
from digital_logic.experiment.models import UserSubject, Exercise, \
    SubjectAssignment
from digital_logic.experiment.service import list_answered_exercise_ids, \
    list_unanswered_exercise_ids

Q_POOL = [1, 2, 9, 16, 17, 18, 19, 21, 22, 27,
          32, 34, 43, 44, 45, 48, 49, 50,
          51, 52, 53, 57, 58, 59, 60, 61, 62]

A_POOL = [4, 5, 11, 25, 31, 39, 40, 54, 56, 63]

STATIC_POOL = [42, 37, 55]

DEFAULT_E_NUM = 14

MONKEY_CATCHER = 64

MONKEY_INDEX = int(DEFAULT_E_NUM / 2)


def initialize_subject_exercises(subject_id, assignment_id):
    subject = UserSubject.get(subject_id)
    assignment = SubjectAssignment.get(assignment_id)

    assignment_phases = app.config['ASSIGNMENT_PHASES']

    if assignment.assignment_phase == assignment_phases[1]:
        assignment.exercise_pool = A_POOL
        db.session.add(assignment)
        db.session.commit()
    else:

        if subject.experiment_group == 0:
            answered_exercises = list_answered_exercise_ids(subject_id, assignment_id)

            total_exercises = DEFAULT_E_NUM
            static_pool = STATIC_POOL

            needed_exercises = total_exercises - len(answered_exercises) - 4

            assessment_qs = A_POOL

            unanswered = list_unanswered_exercise_ids(subject_id, assignment_id)
            unanswered = [q_id for q_id in unanswered]

            exercise_pool = [q_id for q_id in unanswered if q_id not in assessment_qs and q_id not in static_pool]

            monkey_catcher = MONKEY_CATCHER
            monkey_catcher_index = needed_exercises / 2

            exercises = random.sample(exercise_pool,
                                      needed_exercises)
            exercises.insert(monkey_catcher_index, monkey_catcher)

            exercises = static_pool + exercises

            assignment.exercise_pool = exercises

            db.session.add(assignment)
            db.session.commit()
        else:
            assignment.exercise_pool = STATIC_POOL
            assignment.mastery = [0, 0, 0, 0, 3, 3, 3, 3]
            db.session.add(subject)
            db.session.commit()


def get_subject_next_exercise(subject_id, assignment_id):
    subject = UserSubject.get(subject_id)
    assignment = SubjectAssignment.get(assignment_id)

    answered_exercises = list_answered_exercise_ids(subject.id,
                                                    assignment.id)
    total_answered = len(answered_exercises)

    if subject.experiment_group == 0:

        if total_answered < DEFAULT_E_NUM:
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

        elif total_answered > len(assignment.exercise_pool) and total_answered < DEFAULT_E_NUM:
            exercise = Exercise.get(11)
            return exercise
        else:
            return None


