from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL, Email

class RegisterForm(FlaskForm):
    """ Form for registering on our site """

    username = StringField('Username', validators=[InputRequired()]) #length validator
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class LoginForm(FlaskForm):
    """ Form for logging in user into site """

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class AddNotesForm(FlaskForm):
    """ Form for adding notes for the user """

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])

class EditNotesForm(FlaskForm):
    """ Form for editing notes for the user """

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""