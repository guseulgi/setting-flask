from app import db


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String, primary_key=True)
    product_description = db.Column(db.String, nullalble=True)
    product_type = db.Column(db.String, nullable=False)
