from flask import request, session
from flask_restx import Resource, Namespace, fields
from sqlalchemy import exc

from app import db
from models.users import User

user_router = Namespace('Users')

# Models
# Response Models
mpayload = user_router.model('페이로드 모델', {
    "message": fields.String(description='메세지', required=True)
})

mresponse = user_router.model('응답 모델', {
    "success": fields.String(description='성공 여부', required=True),
    "payload": fields.Nested(mpayload)
})

muser_payload = user_router.model('유저 정보 모델', {
    "nickname": fields.String(),
    "id": fields.String(),
    "email": fields.String(),
})

muser_response = user_router.model('유저 모델', {
    "success": fields.String(description='성공 여부', required=True),
    "payload": fields.Nested(muser_payload)
})

# Request Models
msignin = user_router.model('회원가입 모델', {
    "user_info": fields.Nested(user_router.model('회원가입 정보', {
        "nickname": fields.String(description='닉네임'),
        "email": fields.String(description='이메일'),
        "password": fields.String(description='비밀번호'),
        "is_email": fields.String(description='이메일 수신 여부'),
    }))
})

mlogin = user_router.model('로그인 모델', {
    "user_info": fields.Nested(user_router.model('로그인 정보', {
        "email": fields.String(description='이메일'),
        "password": fields.String(description='비밀번호'),
    }))
})


# APIs
@user_router.route('/session')
class GetSession(Resource):
    @user_router.response(model=muser_response, code=200, description='세션 검증 성공')
    @user_router.response(model=mresponse, code=501, description='세션 없음')
    @user_router.response(model=mresponse, code=500, description='알 수 없는 오류')
    def get(self):
        """세션 확인 API"""
        print('session', session)
        print(session.get('userId'), '?')
        print(session['userId'], "session['userId']")

        if 'userId' in session:
            user_id = session['userId']
        else:
            return {
                "success": False,
                "payload": {
                    "meassage": 'No session',
                }
            }, 501

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


@user_router.route('/<user_email>')
class UsersAPI(Resource):
    @user_router.expect(msignin)
    @user_router.response(model=mresponse, code=201, description='회원가입 성공')
    @user_router.response(model=mresponse, code=500, description='알 수 없는 오류')
    def post(self, user_email):
        """ 회원가입 API """
        try:
            request_result = request.json['user_info']
            request_nickname = request_result.get('nickname')
            # request_email = request_result.get('email')
            request_password = request_result.get('password')
            request_is_email = request_result.get('is_email')

            user = User(nickname=request_nickname,
                        email=user_email, password=request_password,
                        is_email=request_is_email)
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
        }, 201

    def put(self, user_email):
        """사용자 수정 API"""
        try:
            request_result = request.json['user_info']
            request_nickname = request_result.get('nickname')
            request_password = request_result.get('password')
            request_coment = request_result.get('coment')

            quser = User.query.filter(User.user_email == user_email)
            cur_user = quser.one_or_none()
            if cur_user is None:
                return {
                    "success": False,
                    "payload": {
                        "message": "No user info"
                    }
                }, 400

            quser.update(dict(user_nickname=request_nickname,
                              user_password=request_password, user_coment=request_coment))
            db.session.commit()

        except Exception as e:
            return {
                "success": False,
                "payload": {
                    "message": f"{e}"
                }
            }, 500

    def delete(self, user_email):
        """사용자 삭제 API"""


@user_router.route('')
class UserAPI(Resource):
    def get(self):
        """전체 사용자 리스트 조회 API"""


@user_router.route('/auth')
class Auth(Resource):
    @user_router.response(model=mresponse, code=200, description='로그아웃 성공')
    def get(self):
        """로그아웃 API"""
        user_id = session['user_id']
        session.pop(user_id, None)

        return {
            "success": True,
            "payload": {
                "message": "Log out OK"
            }
        }, 200

    @user_router.expect(mlogin)
    @user_router.response(model=mresponse, code=200, description='로그인 성공')
    @user_router.response(model=mresponse, code=401, description='사용자 입력 오류')
    @user_router.response(model=mresponse, code=500, description='알 수 없는 오류')
    def post(self):
        """로그인 API"""
        user_info = request.json['user_info']

        try:
            find_user = User.query.filter(
                User.user_email == user_info.get('email')).one_or_none()
            isPw = User.checkPw(find_user,
                                user_info.get('password'))

            if not isPw:
                return {
                    "success": False,
                    "payload": {
                        "message": f"Fail log in - Invalid password"
                    }
                }, 401

            session['userId'] = find_user.user_id
            print("session['userId']", session['userId'])

            db.session.commit()

            return {
                "success": True,
                "payload": {
                    "message": "Log in OK",
                }
            }, 200
        except Exception as e:
            return {
                "success": False,
                "payload": {
                    "message": f"{e}"
                }
            }, 500
