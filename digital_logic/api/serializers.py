from flask_restplus import fields

from ..core import api

subject = api.model('Subject', {
    'id': fields.Integer(readonly=True,
                         description='The unique id of the subject'),
    'assignment_id': fields.String(required=True,
                                   description='The assignment_id of the assignment in Mechanical Turk'),
    'worker_id': fields.String(required=True,
                               description='The worker_id of the subject on Mechanical Turk'),
    'hit_id': fields.String(required=True,
                            description='The hit_id on Mechanical Turk'),
    'experiment_group': fields.String(required=True,
                                      description='The experiment group the subject is in'),
    'status': fields.String(required=False,
                            description='The status of the subject in the experiment'),
    'completion_code': fields.String(required=False, description='The completion code generated for the subject at the end of the experiment')
})

# This is used to setup the response needed for backbone to initalize experiment model for the subject
experiment_data_setup = api.model('ExperimentDataSetup', {
    'id': fields.Integer(readonly=True,
                         description='The unique id of the subject'),
    'assignment_id': fields.String(required=True,
                                   description='The assignment_id of the assignment in Mechanical Turk'),
    'worker_id': fields.String(required=True,
                               description='The worker_id of the subject on Mechanical Turk'),
    'hit_id': fields.String(required=True,
                            description='The hit_id on Mechanical Turk')
})

#
# form_responses = api.model('FormResponses', {})

form_data = api.model('formData', {})
session_data = api.model('sessionData', {})
event_data = api.model('eventData', {})
question_data = api.model('questionData', {})


experiment_data_put = api.model('ExperimentData', {
    'id': fields.Integer(required=True, readonly=True),
    'assignment_id': fields.String(required=True,
                                   description='The assignment_id of the assignment in Mechanical Turk'),
    'worker_id': fields.String(required=True,
                               description='The worker_id of the subject on Mechanical Turk'),
    'hit_id': fields.String(required=True,
                            description='The hit_id on Mechanical Turk'),
    'formData': fields.List(fields.Nested(form_data)),
    'sessionData': fields.List(fields.Nested(session_data)),
    'eventData': fields.List(fields.Nested(event_data)),
    'questionData': fields.List(fields.Nested(question_data))
})
