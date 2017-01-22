from flask import request
from flask_restplus import Resource

from digital_logic.api.parsers import exercises_arguments
from digital_logic.api.serializers import exercise
from digital_logic.core import api
from digital_logic.experiment.exercise import get_subject_next_exercise
from digital_logic.experiment.models import Exercise

ns = api.namespace('exercises',
                   description='Operations related to experiment exercises')


def format_exercise(exercise_model):
    """
    Formats the json that contains the exercise text and answer choices in an
    appropriate manner for the subject. This will remove correctness scores from
    the answers to thwart any attempts of the user to cheat and view the
    response from the web api using devtools.

    :param question_data: the json representation of the exercise
    :return: question
    """
    exercise = dict()
    exercise['id'] = exercise_model.id
    exercise['text'] = exercise_model.data['simple_question']['content']['html']

    choices = exercise_model.data['simple_question']['answer_choices']
    print(choices)
    exercise['choices'] = choices

    exercise['choices'] = [choice for choice in choices]

    return exercise


@ns.route('/<int:exercise_id>')
@ns.response(404, 'Exercise not found')
@ns.param('exercise_id', 'The exercise identifier')
class ExerciseItem(Resource):
    """
    Returns a single exercise. A delete is not allowed
    """

    @ns.doc('get_exercise')
    @ns.marshal_with(exercise)
    def get(self, exercise_id):
        """
        Returns an exercise item
        """
        return Exercise.get(exercise_id)


@ns.route('/next')
@ns.response(404, 'Exercise not found')
class ExperimentExercise(Resource):
    """
    Returns an exercise based on the experiment group and reading section of the
    digital logic textbook.
    """

    @ns.expect(exercises_arguments)
    @ns.marshal_with(exercise)
    def get(self):
        args = exercises_arguments.parse_args(request)
        subject_id = args.get('subject_id')
        section_name = args.get('section_name')
        assignment_id = args.get('assignment_id')
        exercise = get_subject_next_exercise(subject_id, assignment_id)
        formatted_exercise = format_exercise(exercise)
        return formatted_exercise
