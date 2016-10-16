from flask_restplus import Resource

from digital_logic.core import api

ns = api.namespace('subjects', description='Operations related to experiment '
                                           'subjects')


@ns.route('/')
class SubjectCollection(Resource):
    def get(self):
        """
        Returns a list of subjects
        """
        pass
