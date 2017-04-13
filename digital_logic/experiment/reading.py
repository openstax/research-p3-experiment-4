from flask import session


reading_sections = [
    {
        'section_id': 1,
        'name': 'preface',
        'has_exercises': False,
        'exercises': [],
        'next_section': 'introduction'
    },
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
        'has_exercises': True,
        'exercises': [],
        'next_section': 'compound-boolean-expression'
    },
    {
        'section_id': 4,
        'name': 'compound-boolean-expression',
        'has_exercises': True,
        'exercises': ['q14296v1'],
        'next_section': 'summary'
    },
    {
        'section_id': 5,
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


