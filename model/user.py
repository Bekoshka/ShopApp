from sqlalchemy.dialects.postgresql import UUID, TEXT, BOOLEAN
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
import db_session
from db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(TEXT, nullable=False)
    password = sqlalchemy.Column(TEXT, nullable=False)
    fname = sqlalchemy.Column(TEXT, default='', nullable=False)
    lname = sqlalchemy.Column(TEXT, default='', nullable=False)
    sex = sqlalchemy.Column(BOOLEAN, default=True, nullable=False)
    phone = sqlalchemy.Column(TEXT, default='', nullable=False)
    email = sqlalchemy.Column(TEXT, default='', nullable=False)
    address = sqlalchemy.Column(TEXT, default='', nullable=False)
    @classmethod
    def items(cls):
        return {"items": [i.to_dict() for i in db_session.create_session().query(User).all()]}