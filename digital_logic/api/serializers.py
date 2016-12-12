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

exercise = api.model('Exercise', {
    'id': fields.Integer(readonly=True,
                         description='The unique id of the exercise'),
    'qb_id': fields.String(required=True,
                           description='The qbase id of the exercise'),
    'level': fields.Integer(requried=True,
                            description='The difficulty of the exercise'),
    'topic': fields.String(required=True,
                           description='The "tag" of the exercise often used by biglearn in the Question x Topic matrix'),
    'data': fields.String(readonly=True,
                          description='The JSON data which containes all the data about the exercise. This was extracted from Qbase')
})
