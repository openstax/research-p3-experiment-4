from flask import session

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
    {
        'section_id': 1,
        'name': 'preface',
        'has_exercises': False,
        'exercises': [],
        'next_section': 'introduction'
    }
    ,
    {
        'section_id': 2,
        'name': 'introduction',
        'has_exercises': False,
        'exercises': [],
        'next_section': 'boolean-variables'
    },
    {
        'section_id': 3,
        'name': 'boolean-variables',
        'has_exercises': False,
        'exercises': [],
        'next_section': 'logic-gates'
    },
    {
        'section_id': 4,
        'name': 'logic-gates',
        'has_exercises': True,
        'exercises': ['q14462v1', 'q14454v1'],
        'next_section': 'truth-tables'
    },
    {
        'section_id': 5,
        'name': 'truth-tables',
        'has_exercises': False,
        'exercises': [],
        'next_section': 'compound-boolean-expression'
    },
    {
        'section_id': 6,
        'name': 'compound-boolean-expression',
        'has_exercises': True,
        'exercises': ['q14296v1'],
        'next_section': 'circuits-to-truth-tables'
    },
    {
        'section_id': 7,
        'name': 'circuits-to-truth-tables',
        'has_exercises': True,
        'exercises': ['q14274v2'],
        'next_section': 'truth-tables-to-boolean'
    },
    {
        'section_id': 8,
        'name': 'truth-tables-to-boolean',
        'has_exercises': True,
        'exercises': ['q14313v1', 'q14309v2'],
        'next_section': 'summary'
    },
    {
        'section_id': 9,
        'name': 'summary',
        'has_exercises': False,
        'exercises': [],
        'next_section': None
    }
]


def get_section_obj(section_name):
    return [section for section in reading_sections if
            section['name'] == section_name][0]


def initialize_reading_sections():
    sections_completed = 0
    total_sections = len(reading_sections)

    session['reading_sections'] = reading_sections
    session['sections_completed'] = sections_completed
    session['total_sections'] = total_sections

    return True


