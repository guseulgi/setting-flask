from app import db


class Poke(db.Model):
    __tablename__ = 'poke'

    poke_id = db.Column(db.String, primary_key=True)
    poke_productid = db.Column(db.String, db.ForeignKey(
        'product.product_id'), nullable=False)  # 몬콜레 아이디
    poke_name = db.Column(db.String)
    poke_num = db.Column(db.Integer)
    poke_type = db.Column(db.String)
