import re
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField,
                     IntegerField, FieldList)
from wtforms.validators import (DataRequired, Regexp, NumberRange, URL,
                                Length, EqualTo, ValidationError, Email)

from .models import Entry


def date_format(form, field):
    date_match = re.fullmatch(
        r'(?P<month>[\d]{1,2})-(?P<day>[\d]{1,2})-(?P<year>[\d]{4,4})',
        field.data
    )
    if date_match is None:
        raise ValidationError('Date does not fit format 12-23-2018.')
    try:
        month = int(date_match.group('month'))
        day = int(date_match.group('day'))
        year = int(date_match.group('year'))
    except ValueError:
        raise ValidationError('Date doesn\'t not fit format 12-23-2018.')
    if month > 12:
        raise ValidationError('Month in date is out of range.')
    if day > 31:
        raise ValidationError('Day in date is out of range.')
    if year > 2100 or year < 1900:
        raise ValidationError('Get real! A reasonable year please, Time Lord.')


class EntryForm(FlaskForm):
    title = StringField(
        'title',
        validators=[
            DataRequired()
        ]
    )
    date = StringField(
        'date',
        validators=[
            DataRequired(),
            date_format,
        ]
    )
    time_spent = IntegerField(
        'time_spent',
        validators=[
            DataRequired()
        ]
    )
    notes = TextAreaField(
        'notes',
        validators=[
            DataRequired(),
        ]
    )
    resources = FieldList(
        StringField(
            'url',
            validators=[
                DataRequired(),
                URL()
            ],
        ),
        min_entries=1
    )
