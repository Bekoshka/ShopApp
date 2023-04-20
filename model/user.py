import enum

from sqlalchemy import DECIMAL, INTEGER, TEXT, BOOLEAN, Column, ForeignKey, BLOB, UniqueConstraint, TIMESTAMP, DATETIME, \
    func, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
import db_session
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

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(User).all()]}


class ProductCategory(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product_categories'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    product_category_id = Column(INTEGER, ForeignKey('product_categories.id'))
    image = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    price = Column(DECIMAL, nullable=False)
    # discount_id = sqlalchemy.Column(TEXT, nullable=False)
    quantity = Column(INTEGER, nullable=False)
    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}


class CartItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart_items'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    product_id = Column(INTEGER, ForeignKey('products.id'))
    quantity = Column(INTEGER, nullable=False)
    product = relationship("Product")
    __table_args__ = (UniqueConstraint('user_id', 'product_id'), )

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}


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

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}


class OrderItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_items'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    order_id = Column(INTEGER, ForeignKey('orders.id'))
    product_id = Column(INTEGER, ForeignKey('products.id'))
    quantity = Column(INTEGER, nullable=False)
    sum = Column(DECIMAL, nullable=False)
    product = relationship("Product")

    __table_args__ = (UniqueConstraint('order_id', 'product_id'),)

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}