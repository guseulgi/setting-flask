from app import bcrypt
from app import db
from controllers.randoms import randomStr


class User(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    user_nickname = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)

    def __init__(self, nickname, email, password):
        self.user_id = randomStr()
        self.user_nickname = nickname
        self.user_email = email
        self.user_password = bcrypt.generate_password_hash(password)

    def getId(self):
        return self.user_id
