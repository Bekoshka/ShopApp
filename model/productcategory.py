from sqlalchemy import Column, INTEGER, TEXT
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class ProductCategory(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product_categories'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
