from transitions import Machine

# reading_sections = [
#     'preface',
#     'introduction',
#     'boolean-variables',
#     'logic-gates',
#     'truth-tables',
#     'compound-boolean-expression',
#     'circuits-to-truth-tables',
#     'truth-tables-to-boolean',
#     'summary'
# ]

reading_sections = [
    {'section_id': 1,'name': 'preface', 'has_exercises': False, 'exercises': []},
    {'section_id': 2,'name': 'introduction', 'has_exercises': False, 'exercises': []},
    {'section_id': 3,'name': 'boolean-variables', 'has_exercises': False, 'exercises': []},
    {'section_id': 4,'name': 'logic-gates', 'has_exercises': True, 'exercises': ['q14462v1', 'q14454v1']},
    {'section_id': 5,'name': 'truth-tables', 'has_exercises': False, 'exercises': []},
    {'section_id': 6,'name': 'compound-boolean-expression', 'has_exercises': True, 'exercises': ['q14296v1']},
    {'section_id': 7,'name': 'circuits-to-truth-tables', 'has_exercises': True, 'exercises': ['q14274v2']},
    {'section_id': 8,'name': 'truth-tables-to-boolean', 'has_exercises': True, 'exercises': ['q14313v1', 'q14309v2']},
    {'section_id': 9,'name': 'summary', 'has_exercises': False}
]


class Reading(object):
    states = ['preface', 'introduction', 'boolean_variables']

    transitions = [
        {
            'trigger': 'advance',
            'source': 'preface',
            'dest': 'introduction',
        },
        {
            'trigger': 'advance',
            'source': 'introduction',
            'dest': 'boolean_variables',
        }
    ]

    def __init__(self):
        self.machine = Machine(model=self,
                               states=Reading.states,
                               transitions=Reading.transitions,
                               initial='preface')

