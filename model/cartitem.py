from sqlalchemy import Column, INTEGER, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class CartItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart_items'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    product_id = Column(INTEGER, ForeignKey('products.id'))
    quantity = Column(INTEGER, nullable=False)
    product = relationship("Product")
    __table_args__ = (UniqueConstraint('user_id', 'product_id'), )
