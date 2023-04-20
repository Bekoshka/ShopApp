from sqlalchemy import UniqueConstraint, DECIMAL, Column, INTEGER, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class OrderItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_items'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    order_id = Column(INTEGER, ForeignKey('orders.id'))
    product_id = Column(INTEGER, ForeignKey('products.id'))
    quantity = Column(INTEGER, nullable=False)
    sum = Column(DECIMAL, nullable=False)
    product = relationship("Product")

    __table_args__ = (UniqueConstraint('order_id', 'product_id'),)
