from sqlalchemy import INTEGER, TEXT, BOOLEAN, Column, UniqueConstraint
from sqlalchemy_serializer import SerializerMixin
from db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    login = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    is_admin = Column(BOOLEAN, default=False, nullable=False)
    fname = Column(TEXT, default='', nullable=False)
    lname = Column(TEXT, default='', nullable=False)
    sex = Column(BOOLEAN, default=True, nullable=False)
    phone = Column(TEXT, default='', nullable=False)
    email = Column(TEXT, default='', nullable=False)
    address = Column(TEXT, default='', nullable=False)
    __table_args__ = (UniqueConstraint('login'),)
