from flask import Flask, render_template, redirect, \
    request, make_response, session, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.user import Astronaut
import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms.user_login import AstronautLog
from forms.add_job import JobForm
from forms.add_dept import DeptForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AstronautLog()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.astronaut_login.data).first()
        if user and user.check_password(form.astronaut_password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            start_date=datetime.datetime.now()
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы', form=form, header='Add Job')


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == 'GET':
        chosen_job = db_sess.query(Jobs).filter(Jobs.id == id,
                                                (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
        if chosen_job:
            form.job.data = chosen_job.job
            form.collaborators.data = chosen_job.collaborators
            form.work_size.data = chosen_job.work_size
            form.team_leader.data = chosen_job.team_leader
        else:
            abort(404)
    if form.validate_on_submit():
        chosen_job = db_sess.query(Jobs).filter(Jobs.id == id,
                                                (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
        if chosen_job:
            chosen_job.job = form.job.data
            chosen_job.collaborators = form.collaborators.data
            chosen_job.work_size = form.work_size.data
            chosen_job.is_finished = form.is_finished.data
            chosen_job.team_leader = form.team_leader.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Редактирование работы', form=form, header='Edit Job')


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    chosen_job = db_sess.query(Jobs).filter(Jobs.id == id,
                                            (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
    if chosen_job:
        db_sess.delete(chosen_job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/success')
def success():
    return render_template('success_registration.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/departments')
def departments():
    depts = db_sess.query(Departments).all()
    leads = list(map(lambda x: (x.name, x.surname),
                     map(lambda x: db_sess.query(User).filter(User.id == x.chief).first(),
                         depts)))
    return render_template('departments.html', depts=depts, leads=leads)


@app.route('/add_dept', methods=['GET', 'POST'])
@login_required
def add_dept():
    form = DeptForm()
    if form.validate_on_submit():
        new_dept = Departments(
            email=form.email.data,
            chief=form.chief.data,
            members=form.members.data,
            title=form.title.data
        )
        print(form.email.data,
            form.chief.data,
            form.members.data, form.title.data)
        db_sess.add(new_dept)
        db_sess.commit()
        return redirect('/')
    return render_template('add_dept.html', form=form, header='Add department')


@app.route('/delete_dept/<int:id>')
@login_required
def delete_dept(id):
    chosen_dept = db_sess.query(Departments).filter(Departments.id == id,
                                                    (
                                                            Departments.chief == current_user.id | current_user.id == 1)).first()
    if chosen_dept:
        db_sess.delete(chosen_dept)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_dept/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dept(id):
    form = DeptForm()
    if request.method == 'GET':
        chosen_dept = db_sess.query(Departments).filter(Departments.id == id,
                                                        (
                                Departments.chief == current_user.id | current_user.id == 1)).first()
        if chosen_dept:
            form.chief.data = chosen_dept.chief
            form.members.data = chosen_dept.members
            form.title.data = chosen_dept.title
            form.email.data = chosen_dept.email
        else:
            abort(404)
    if form.validate_on_submit():
        chosen_dept = db_sess.query(Departments).filter(Departments.id == id,
                                                        (
                                Departments.chief == current_user.id | current_user.id == 1)).first()
        if chosen_dept:
            chosen_dept.chief = form.chief.data
            chosen_dept.members = form.members.data
            chosen_dept.title = form.title.data
            chosen_dept.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_dept.html', title='Редактирование департамента', form=form, header='Edit Department')


def main():
    app.run()


if __name__ == '__main__':
    main()
