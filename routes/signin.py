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

muser_payload = Signin.model('유저 정보 모델', {
    "nickname": fields.String(),
    "id": fields.String(),
    "email": fields.String(),
})

muser_response = Signin.model('유저 모델', {
    "success": fields.String(description='성공 여부', required=True),
    "payload": fields.Nested(muser_payload)
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
class GetSession(Resource):
    @Signin.response(model=muser_response, code=200, description='세션 검증 성공')
    @Signin.response(model=mresponse, code=500, description='알 수 없는 오류')
    def get(self):
        """세션 확인 API"""
        user_id = session['userId']

        try:
            result = User.query.filter(User.user_id == user_id).one()
        except Exception as e:
            return {
                "success": False,
                "payload": {
                    "meassage": e,
                }
            }, 500

        return {
            "success": True,
            "payload": {
                "meassage": "Collect User",
                "id": result.user_id,
                "nickname": result.user_nickname,
                "email": result.user_email
            }
        }, 200


@Signin.route('/signup')
class Signup(Resource):
    @Signin.expect(msignin)
    @Signin.response(model=mresponse, code=200, description='회원가입 성공')
    @Signin.response(model=mresponse, code=500, description='알 수 없는 오류')
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
class Login(Resource):
    @Signin.expect(mlogin)
    @Signin.response(model=mresponse, code=200, description='로그인 성공')
    @Signin.response(model=mresponse, code=400, description='사용자 입력 오류')
    @Signin.response(model=mresponse, code=500, description='알 수 없는 오류')
    def post(self):
        """로그인 API"""
        user_info = request.json['user_info']

        try:
            find_user = User.query.filter(
                User.user_email == user_info.get('email')).one_or_none()
            isPw = User.checkPw(find_user,
                                user_info.get('password'))

            session['userId'] = find_user.user_id
            print("session['userId']", session['userId'])
            # TODO 세션이 쿠키로 넘어가지 않음

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
class Logout(Resource):
    @Signin.response(model=mresponse, code=200, description='로그아웃 성공')
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
