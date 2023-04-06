from sqlalchemy.dialects.postgresql import UUID, TEXT
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
import db_session
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(TEXT)
    password = sqlalchemy.Column(TEXT)


    @classmethod
    def items(cls):
        """ Returns all Todo instances in a JSON
            Flask response.
        """
        return {"items": [i.to_dict() for i in db_session.create_session().query(User).all()]}
