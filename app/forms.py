from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField("Description", validators=[InputRequired()])
    photo = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Images only!')
        ]
    )

class NewPostForm(FlaskForm):
    caption = TextAreaField("Description", validators=[InputRequired()])
    photo = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Images only!')
        ]
    )

