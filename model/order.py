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

    @property
    def label(self):
        translate = {
            "new": "Новый",
            "packing": "Собирается",
            "delivery": "В пути",
            "done": "Выполнен",
            "canceled": "Отменен"
        }
        return translate[self.name]


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    status = Column(Enum(OrderStatus))
    address = Column(TEXT, nullable=False)
    phone = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    time = Column(DATETIME(timezone=True), server_default=func.now())
    sum = Column(DECIMAL, nullable=False)
