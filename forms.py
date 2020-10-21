"""Forms for cicerone app"""

from wtforms import SelectField, StringField, PasswordField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange

class SignupForm(FlaskForm):
    """Form for signing-up a new user"""

    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging-in a user"""

    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])


class ReviewForm(FlaskForm):
    """Form for writing a review"""
    rating = IntegerField("Rating 1 - 5:", validators = [NumberRange(min=1,max=5)])
    text = StringField("Review: ", validators = [InputRequired()])
