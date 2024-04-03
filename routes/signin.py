from flask import request, jsonify, session
from flask_restx import Resource, Namespace, fields
from sqlalchemy import exc

from app import db
from models.users import User

Signin = Namespace('Signin')

# Models
# Response Models
mpayload = Signin.model('페이로드 모델', {
    "message": fields.String(description='메세지', required=True)
})

mresponse = Signin.model('응답 모델', {
    "success": fields.String(description='성공 여부', required=True),
    "payload": fields.Nested(mpayload)
})

# Request Models
msignin = Signin.model('회원가입 모델', {
    "user_info": fields.Nested(Signin.model('회원가입 정보', {
        "nickname": fields.String(description='닉네임'),
        "email": fields.String(description='이메일'),
        "password": fields.String(description='비밀번호'),
        "is_email": fields.String(description='이메일 수신 여부'),
    }))
})

mlogin = Signin.model('로그인 모델', {
    "user_info": fields.Nested(Signin.model('로그인 정보', {
        "email": fields.String(description='이메일'),
        "password": fields.String(description='비밀번호'),
    }))
})


# APIs
@Signin.route('/session')
@Signin.doc(responses={
    200: '성공',
    500: '알 수 없는 오류'
})
class GetSession(Resource):
    @Signin.marshal_with(mresponse)
    def get(self):
        """세션 확인 API"""
        user_id = session['user_id']

        try:
            result = User.query.filter(User.user_id == user_id).one()
        except exc.SQLAlchemyError as e:
            return {
                "success": False,
                "payload": {
                    "meassage": type(e),
                }
            }, 500

        return {
            "success": True,
            "payload": {
                "meassage": "Collect User",
            }
        }, 200


@Signin.route('/signup')
@Signin.doc(responses={
    200: '성공',
    500: '알 수 없는 오류'
})
class Signup(Resource):
    @Signin.expect(msignin)
    @Signin.marshal_with(mresponse)
    def post(self):
        """ 회원가입 API """
        try:
            request_result = request.json['user_info']
            request_nickname = request_result.get('nickname')
            request_email = request_result.get('email')
            request_password = request_result.get('password')
            request_is_email = request_result.get('is_email')

            user = User(nickname=request_nickname,
                        email=request_email, password=request_password, is_email=request_is_email)
            db.session.add(user)

        except Exception as e:
            return {
                "success": False,
                "payload": {
                    "message": e
                }
            }, 500

        db.session.commit()
        return {
            "success": True,
            "payload": {
                "message": "Sign in OK!"
            }
        }, 200


@Signin.route('/signin')
@Signin.doc(responses={
    200: '성공',
    500: '알 수 없는 오류',
    501: '입력 불일치'
})
class Login(Resource):
    @Signin.expect(mlogin)
    @Signin.marshal_with(mresponse)
    def post(self):
        """로그인 API"""
        user_info = request.json['user_info']

        try:
            find_user = User.query.filter(
                User.user_email == user_info.get('email')).one_or_none()
            isPw = User.checkPw(find_user,
                                user_info.get('password'))

            session['userId'] = find_user.user_id

            if not isPw:
                return {
                    "success": False,
                    "payload": {
                        "message": f"Fail log in - Invalid password"
                    }
                }, 501
        except Exception as e:
            return {
                "success": False,
                "payload": {
                    "message": f"Fail log in - {e}"
                }
            }, 500

        return {
            "success": True,
            "payload": {
                "message": "Log in OK",
            }
        }, 200


@Signin.route('/signout')
@Signin.doc(responses={
    200: '성공'
})
class Logout(Resource):
    @Signin.marshal_with(mresponse)
    def post(self):
        """로그아웃 API"""
        user_id = session['user_id']
        session.pop(user_id)

        return {
            "success": True,
            "payload": {
                "message": "Log out OK"
            }
        }, 200
