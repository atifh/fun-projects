#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>

import re

from wtforms import *
from wtforms.validators import ValidationError

# Regex borrowed from Django forms
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_valid_email(form, field):
    """Validates email field
    """
    email = field.data
    if email:
        if not email_re.match(email):
            raise ValidationError(u'Enter a valid email')
    else:
        raise ValidationError(u'This field is required')
    return field


class RegistrationForm(Form):
    """A simple class for registration form
    """
    username = TextField('Username', [validators.length(min=4, max=25)])
    password = PasswordField('Password', [validators.length(min=5, max=25)])
    first_name = TextField(u'First Name', validators=[validators.required()])
    last_name  = TextField(u'Last Name', validators=[validators.optional()])
    # Custom EmailField written
    email = TextField('Email Address', [is_valid_email])
    avatar = FileField(u'Image File')
    birthday = DateTimeField('Your Birthday',  validators=[validators.optional()], format='%m/%d/%y')


