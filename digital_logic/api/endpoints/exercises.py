from flask_restplus import Resource

from digital_logic.api.serializers import exercise
from digital_logic.core import api
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
