# forms.py


from flask_wtf import Form
from wtforms import (TextField, DateField, IntegerField, SelectField,
                     PasswordField)
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QueryFXQuotes(Form):

    source_currency = SelectField('Source Currency',
                           validators=[DataRequired()],
                           choices=[('All', 'All'), ('GBP', 'GBP')])

    target_currency = SelectField('Target Currency',
                           validators=[DataRequired()],
                           choices=[('All', 'All'), ('USD', 'USD')])

    source_value = SelectField('Source Value',
                           validators=[DataRequired()],
                           choices=[('All', 'All'), ('100', '100')])