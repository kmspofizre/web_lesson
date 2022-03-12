from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class Astronaut(FlaskForm):
    astronaut_login = StringField('Login / email', validators=[DataRequired()])
    astronaut_password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired()])
    astronaut_surname = StringField('Surname', validators=[DataRequired()])
    astronaut_name = StringField('Name', validators=[DataRequired()])
    astronaut_age = IntegerField('Age', validators=[DataRequired()])
    astronaut_position = StringField('Position', validators=[DataRequired()])
    astronaut_speciality = StringField('Speciality', validators=[DataRequired()])
    astronaut_address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')
