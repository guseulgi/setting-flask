from app import bcrypt
from app import db


class Likelist(db.Model):
    __tablename__ = 'likelist'

    lk_id = db.Column(db.String, primary_key=True)
    lk_userid = db.Column(db.String)  # 사용자 아이디
    lk_pokeid = db.Column(db.String)  # 포켓몬 아이디
    lk_productid = db.Column(db.String)  # 몬콜레 아이디
    lk_name = db.Column(db.String)
