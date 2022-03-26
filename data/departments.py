import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief_id = orm.relation('User')