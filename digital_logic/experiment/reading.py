from flask import render_template
from pyquery import PyQuery as pq

from digital_logic.exceptions import SectionNotFound
from ._constants import BEGINNER_POOL, INTERMEDIATE_POOL

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
        'level': 'BEGINNER',
        'has_exercises': True,
        'exercises': BEGINNER_POOL,
        'next_section': 'compound-boolean-expression'
    },
    {
        'section_id': 4,
        'name': 'compound-boolean-expression',
        'level': 'INTERMEDIATE',
        'has_exercises': True,
        'exercises': INTERMEDIATE_POOL,
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


def render_textbook_text(section='all'):
    """
    Responsible for rendering the textbook markdown and returning either the
    text as a whole or a specific section.

    :param section: the section of the text
    :return: html of the textbook or section
    """
    textbook_text = render_template('textbook/digital_logic.md')

    if section is 'all':
        return textbook_text
    else:
        text = pq(textbook_text)
        section_text = text('.' + section)
        if section_text:
            return section_text.html()
        else:
            raise SectionNotFound
