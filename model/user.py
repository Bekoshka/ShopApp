from sqlalchemy import DECIMAL, INTEGER, TEXT, BOOLEAN, Column, ForeignKey, BLOB
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
    image = Column(BLOB, nullable=False)
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

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = product_id = Column(INTEGER, ForeignKey('users.id'))
    status = Column(INTEGER, nullable=False)

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

    @classmethod
    def items(cls):
        with db_session.create_session() as session:
            return {"items": [i.to_dict() for i in session.query(Product).all()]}