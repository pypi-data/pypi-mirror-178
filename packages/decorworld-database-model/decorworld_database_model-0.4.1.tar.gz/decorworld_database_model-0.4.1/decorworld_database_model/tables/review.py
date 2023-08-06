from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load
from .image import ImageSchema

from .base import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    name = Column(String(30), nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String(100), nullable=True)


class ReviewSchema(Schema):

    model_class = Review

    id = fields.Integer()
    product_id = fields.Integer(data_key='productId')
    name = fields.String()
    rating = fields.Integer()
    description = fields.String()

    image = fields.Nested(ImageSchema)

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)
