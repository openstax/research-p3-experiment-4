from flask import render_template
from flask_restplus import Resource
from pyquery import PyQuery as pq

from digital_logic.core import api
from digital_logic.exceptions import SectionNotFound

ns = api.namespace('textbook',
                   description='The api endpoint for rendering portions of the '
                               'digital logic textbook')


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


@ns.route('/')
class Textbook(Resource):
    """
    Renders and returns the entire digital logic textbook
    """

    def get(self):
        textbook_text = render_textbook_text(section='all')

        response = dict(text=textbook_text)

        return response


@ns.route('/<string:section>')
@ns.param('section', 'The section of the textbook to return')
class TextbookSection(Resource):
    """
    Retrieves a specific section of the digital logic textbook
    """

    def get(self, section):

        section_html = render_textbook_text(section=section)

        return dict(html=section_html, section=section)
