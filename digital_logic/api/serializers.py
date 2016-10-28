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
                                      description='The experiment group the subject is in')
})
