from sqlalchemy import Column, INTEGER, ForeignKey, TEXT, DECIMAL
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    product_category_id = Column(INTEGER, ForeignKey('product_categories.id'))
    image = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    price = Column(DECIMAL, nullable=False)
    quantity = Column(INTEGER, nullable=False)
