from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mars_explorer.db")
db_sess = db_session.create_session()


captain = User()
captain.surname = 'Scott'
captain.name = 'Ridley'
captain.age = 21
captain.position = 'captain'
captain.speciality = 'researhc engineer'
captain.address = 'module_1'
captain.email = 'scott_chief@mars.org'

lead_scientist = User()
lead_scientist.surname = 'Phineas'
lead_scientist.name = 'Welles'
lead_scientist.age = 47
lead_scientist.position = 'deputy captain'
lead_scientist.speciality = 'lead_scientist'
lead_scientist.address = 'module_2'
lead_scientist.email = 'Phells@mars.org'

security = User()
security.surname = 'Isaac'
security.name = 'Clark'
security.age = 49
security.position = 'Sergeant'
security.speciality = 'security'
security.address = 'module_3'
security.email = 'DeadSpace@mars.org'

motivator = User()
motivator.name = 'Tyler'
motivator.surname = 'Durden'
motivator.age = 34
motivator.position = 'Lead Motivator'
motivator.speciality = 'Self destruction'
motivator.address = 'module_8'
motivator.email = 'best_soap@mars.org'
db_sess.add(captain)
db_sess.add(lead_scientist)
db_sess.add(security)
db_sess.add(motivator)
db_sess.commit()


def main():
    app.run()


if __name__ == '__main__':
    main()