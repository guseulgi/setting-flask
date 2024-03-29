from app import bcrypt
from app import db
from controllers.randoms import randomStr


class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.String, primary_key=True)
    user_nickname = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    user_is_email = db.Column(db.String(1), nullable=False, default='N')

    def __init__(self, nickname, email, password, is_email):
        self.user_id = randomStr()
        self.user_nickname = nickname
        self.user_email = email
        self.user_password = bcrypt.generate_password_hash(password)
        self.user_is_email = is_email

    """ 아이디 리턴 함수 """

    def getId(self):
        return self.user_id

    """ 비밀번호 확인 함수 """

    def checkPw(self, user_password):
        return bcrypt.check_password_hash(user_password, self.user_password)
