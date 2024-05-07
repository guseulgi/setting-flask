from app import db


class Likelist(db.Model):
    __tablename__ = 'likelist'

    lk_id = db.Column(db.String, primary_key=True)
    lk_userid = db.Column(db.String, db.ForeignKey(
        'users.user_id'), nullable=False)  # 사용자 아이디
    lk_productid = db.Column(db.String, db.ForeignKey(
        'product.product_id'), nullable=False)  # 몬콜레 아이디
    lk_pokeid = db.Column(db.String)  # 포켓몬 아이디
    lk_pokename = db.Column(db.String)
