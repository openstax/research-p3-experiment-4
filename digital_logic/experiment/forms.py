import flask_wtf as WTF

from wtforms.widgets import html5 as widget
from wtforms.fields import RadioField, SelectField, TextField, TextAreaField, \
    IntegerField, StringField
from wtforms.validators import Length, DataRequired, NumberRange

skill_levels = ('Zero', 'A little', 'Some', 'A lot')


def get_age_choices():
    choices = [(a, a) for a in range(10, 120)]
    return choices


def get_education_choices():
    choices = [('School',
                'Grammar School, '
                'High School or equivalent'),
               ('Vocational',
                'Vocational/Technical School (2 year)'),
               ('College',
                'Some College'),
               ('Graduate',
                'College Graduate (4 year)'),
               ('Masters',
                'Master\'s Degree (MS)'),
               ('Doctoral',
                'Doctoral Degree (PhD)'),
               ('Professional',
                'Professional Degrees (MD, JD, etc.)')]
    return choices


class GatesRangeField(IntegerField):
    """
    Represents an ``<input type="range">``.
    """
    widget = widget.RangeInput(step='10')


class DemographyForm(WTF.FlaskForm):
    skill_level = RadioField(u'Skill level',
                             validators=[DataRequired()],
                             choices=list(zip(skill_levels, skill_levels)))

    english_level = RadioField(u'English proficiency',
                         validators=[DataRequired()],
                         choices=[('t',
                                   "Yes. English IS my first language"),
                                  ('f',
                                   "No. English IS NOT my first language.")])

    age = SelectField(u'Age',
                      validators=[DataRequired()], coerce=int, choices=get_age_choices())

    gender = StringField(u'Gender',
                         validators=[
                             DataRequired(),
                             Length(max=255)])

    education = SelectField(u'Education',
                            validators=[DataRequired()], choices=get_education_choices())


class FinalizeForm(WTF.FlaskForm):
    did_cheat = RadioField(u'External references',
                           validators=[DataRequired()],
                           choices=[('t',
                                     "Yes, I referred to the text, notes, "
                                     "external sources or other aids "
                                     "while answering the questions"),
                                    ('f',
                                     "No, I did not refer to the text, notes, "
                                     "external sources or other aids "
                                     "while answering the questions")])

    comments = TextAreaField(u'Comments')


class PredictionsForm(WTF.Form):
    overall = GatesRangeField('Overall Score',
                              validators=[NumberRange(min=0, max=100)])
    basics = GatesRangeField('Basic Definitions',
                             validators=[NumberRange(min=0, max=100)])
    expressions = GatesRangeField('Expressions',
                                  validators=[NumberRange(min=0, max=100)])
    circuits = GatesRangeField('Circuits',
                               validators=[NumberRange(min=0, max=100)])
    truth_tables = GatesRangeField('Truth Tables',
                                   validators=[NumberRange(min=0, max=100)])
