__author__ = 'shahryar_slg'

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(Form):
    username = StringField('username',
                           validators=[DataRequired(message="pleas enter a username")])

    phone_number = IntegerField('Phone Number',
                                validators=[DataRequired(message="pls , enter your phone number")])

    email = StringField('Email',
                        validators=[DataRequired(message="email is required!"),
                                    Email(message="this is not an Email!!")])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired(
                                     message="Really?? Could you imagine a sign up without a password provided??"),
                                 EqualTo(fieldname='repeat_password', message="passwords must match")])

    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired(message='should not be empty!')])

    submit = SubmitField('Sign up')