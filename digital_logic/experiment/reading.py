from transitions import Machine

reading_sections = [
    'preface',
    'introduction',
    'boolean-variables',
    'logic-gates',
    'truth-tables',
    'compound-boolean-expression',
    'circuits-to-truth-tables',
    'truth-tables-to-boolean',
    'summary'
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

