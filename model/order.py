import enum

from sqlalchemy import Column, INTEGER, ForeignKey, Enum, TEXT, DATETIME, DECIMAL, func
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class OrderStatus(enum.Enum):
    new = 1
    packing = 2
    delivery = 3
    done = 4
    canceled = 5


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    status = Column(Enum(OrderStatus))
    address = Column(TEXT, nullable=False)
    time = Column(DATETIME(timezone=True), server_default=func.now())
    sum = Column(DECIMAL, nullable=False)
