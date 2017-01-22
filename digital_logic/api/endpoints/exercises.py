from flask import request
from flask_restplus import Resource

from digital_logic.api.parsers import exercises_arguments
from digital_logic.api.serializers import exercise
from digital_logic.core import api
from digital_logic.experiment.exercise import get_subject_next_exercise
from digital_logic.experiment.models import Exercise

ns = api.namespace('exercises',
                   description='Operations related to experiment exercises')


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
        return exercise
