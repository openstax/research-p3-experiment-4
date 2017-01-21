from transitions import Machine

reading_sections = ['preface', 'introduction', 'boolean-variables']


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

