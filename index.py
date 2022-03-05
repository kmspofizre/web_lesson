from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    cap_id = StringField('id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    astr_id = StringField('id астронавта', validators=[DataRequired()])
    astr_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


sp = ['инженер-исследователь', 'пилот', 'строитель']
anc = {
    'Фамилия': 'Watny',
    'Имя': 'Mark',
    'Образование': 'Выше среднего',
    'Профессия': 'штурман марсохода',
    'Пол': 'male',
    'Мотивация': 'Всегда мечтал застрять на Марсе!',
    'Готовы остаться на Марсе?': True
}


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['title'] = 'Домашняя страница'
    param['style'] = f"rel=stylesheet href={url_for('static', filename='css/style.css')}"
    return render_template('base.html', **param)


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param['prof'] = prof
    param['spaceship_1'] = f"src={url_for('static', filename='img/spaceship_1.jpg')}"
    param['spaceship_2'] = f"src={url_for('static', filename='img/spaceship_2.jpg')}"
    return render_template('index.html', **param)


@app.route('/list_prof/<list_type>')
def list_maker(list_type):
    return render_template('index.html', profs=sp, lt=list_type)


@app.route('/answer')
@app.route('/auto_answer')
def reminder():
    return render_template('index.html', anc=anc)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
