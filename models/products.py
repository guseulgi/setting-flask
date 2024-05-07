from app import db
from sqlalchemy.orm import relationship


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String, primary_key=True)
    product_description = db.Column(db.String, nullable=True)
    product_type = db.Column(db.String, nullable=False)

# TODO 관계성
    likelist = relationship("likelist")
    pokes = relationship('poke', backref="poke", uselist=False)
