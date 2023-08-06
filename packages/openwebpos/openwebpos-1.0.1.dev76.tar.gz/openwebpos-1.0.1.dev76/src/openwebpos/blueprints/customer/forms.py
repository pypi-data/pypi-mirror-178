from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PhoneSearchForm(FlaskForm):
    """
    Form for searching customer by phone number

    Extends:
        FlaskForm

    Variables:
        phone {StringField} -- Phone number
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for searching customer by phone number

    Example:
        >>> form = PhoneSearchForm()
    """
    phone = StringField('Phone', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Search')
