from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import Astronaut


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init(f"db/mars_explorer.db")
db_sess = db_session.create_session()


@app.route('/')
@app.route('/index')
def job_list():
    jobs_list = list(db_sess.query(Jobs).all())
    leads = list(map(lambda x: (x.name, x.surname),
                     map(lambda x: db_sess.query(User).filter(User.id == x.team_leader).first(),
                     jobs_list)))
    return render_template('jobs.html', jobs_list=jobs_list, leads=leads)


@app.route('/success')
def success():
    return render_template('success_registration.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    astronaut_form = Astronaut()
    if astronaut_form.validate_on_submit():
        if astronaut_form.astronaut_password.data != astronaut_form.repeat_password.data:
            return render_template('registration.html', title='Регистрация',
                                   astronaut_form=astronaut_form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == astronaut_form.astronaut_login.data).first():
            return render_template('registration.html', title='Регистрация',
                                   astronaut_form=astronaut_form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=astronaut_form.astronaut_name.data,
            surname=astronaut_form.astronaut_surname.data,
            email=astronaut_form.astronaut_login.data,
            speciality=astronaut_form.astronaut_speciality.data,
            position=astronaut_form.astronaut_position.data,
            address=astronaut_form.astronaut_address.data,
            age=astronaut_form.astronaut_age.data
        )
        user.set_password(astronaut_form.astronaut_password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/success')
    return render_template('registration.html', title='Регистрация', astronaut_form=astronaut_form)


def main():
    app.run()


if __name__ == '__main__':
    main()
