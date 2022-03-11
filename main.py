from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init(f"db/mars_explorer.db")
db_sess = db_session.create_session()
#n1 = len(max(db_sess.query(Jobs).all(),
        #     key=lambda x: len(x.collaboration.split(', '))).collaboration.split(', '))
#all_leaders = map(lambda x: x.team_leader,
        #          filter(lambda x: len(x.collaboration.split(', ')) == n1,
                 #        db_sess.query(Jobs).all()))
#print('\n'.join(map(lambda x: f'{x.name} {x.surname}',
        #            db_sess.query(User).filter(User.id.in_(all_leaders)))))


@app.route('/')
@app.route('/index')
def job_list():
    jobs_list = list(db_sess.query(Jobs).all())
    leads = list(map(lambda x: (x.name, x.surname),
                     map(lambda x: db_sess.query(User).filter(User.id == x.team_leader).first(),
                     jobs_list)))
    return render_template('jobs.html', jobs_list=jobs_list, leads=leads)


def main():
    app.run()


if __name__ == '__main__':
    main()