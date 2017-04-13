from flask_restplus import reqparse

exercises_arguments = reqparse.RequestParser()
exercises_arguments.add_argument('subject_id', type=int, required=True, help='The subject identifier')
exercises_arguments.add_argument('section_name', type=str, required=True, help='The section of the textbook')
exercises_arguments.add_argument('assignment_id', type=int, required=True, help='The assignment id for the subject')
