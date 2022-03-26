from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class DeptForm(FlaskForm):
    title = StringField('Department title')
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members')
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Добавить')