import json

from flask import request
from flask_restplus import Resource

from digital_logic.api.serializers import (subject,
                                           experiment_data_setup,
                                           experiment_data_put)
from digital_logic.core import api, db
from digital_logic.models import Subject, create_subject, update_subject

ns = api.namespace('subjects',
                   description='Operations related to experiment subjects')


@ns.route('/')
class SubjectCollection(Resource):
    """
    Shows a list of all subjects, and allows a POST to create new subjects
    """

    @ns.marshal_list_with(subject, envelope='collection')
    def get(self):
        """
        Returns a list of subjects
        """
        return Subject.all()

    @ns.doc('create_subject')
    @ns.expect(subject, validate=True)
    @ns.marshal_with(subject, code=201)
    def post(self):
        """
        Creates a subject and returns the created item
        """
        sub = create_subject(request.json)
        return sub, 201


@ns.route('/<int:subject_id>')
@ns.response(404, 'Subject not found')
@ns.param('subject_id', 'The subject identifier')
class SubjectItem(Resource):
    """Show a single subject. A delete is not allowed"""

    @ns.doc('get_subject')
    @ns.marshal_with(subject)
    def get(self, subject_id):
        """
        Returns a subject item
        """
        return Subject.get(subject_id)

    @ns.expect(subject)
    @ns.marshal_with(subject)
    @ns.response(204, 'Subject successfully updated.')
    def put(self, subject_id):
        """
        Updates a subject's data in the database

        * Send a JSON object with the new item in the request body.

        ```
        {
            "worker_id": "debug231G32"
        }
        ```

        * Specify the Subject_id of the subject to modify in the request URL path.
        """
        posted = request.get_json()
        sub = update_subject(subject_id, posted)
        return sub, 204


@ns.route('/data/<int:subject_id>')
@ns.response(404, 'Subject not found')
class SubjectExperimentData(Resource):
    """
    This endpoint is designed to only interact with the data_string field as a
    json payload. The data_string field is a field on the Subject table and
    is used separately to save experiment data. This is designed specifically
    to be used with a backbone.js model.
    """

    @ns.doc('get_subject')
    @ns.marshal_with(experiment_data_setup)
    def get(self, subject_id):
        """
        Returns a subject item
        """
        sub = Subject.get(subject_id)

        try:
            resp = json.loads(sub.data_string)
        except:
            resp = dict(
                id=sub.id,
                assignment_id=sub.assignment_id,
                worker_id=sub.worker_id,
                hit_id=sub.hit_id
            )

        return resp

    @ns.expect(experiment_data_put, validate=True)
    @ns.marshal_with(experiment_data_put)
    @ns.response(204, 'Experiment data successfully updated.')
    def put(self, subject_id):
        """
        Updates a subject's data_string in the database via backbone.js model
        """
        posted = request.get_json()
        sub = Subject.get(subject_id)

        if hasattr(request, 'json'):
            sub.data_string = json.dumps(posted)
            db.session.add(sub)
            db.session.commit()
        return sub, 204
