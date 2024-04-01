from flask import request, jsonify, session
from flask_restx import Resource, Namespace
from sqlalchemy import exc

from app import db
from models.users import User

Signin = Namespace('Signin')

"""
Response JSON - application/json
{
  success: True or False,
  if True: {
    payload: { ... }
  }
  else: {
    code: Integer, 
    message: String
  }
}
"""


@Signin.route('/session')
class GetSession(Resource):
    def get(self):
        """세션 확인 API"""
        user_id = session['user_id']

        try:
            result = User.query.filter(User.user_id == user_id).one()
        except exc.SQLAlchemyError as e:
            return jsonify({
                "success": False,
                "payload": {
                    "meassage": type(e),

                }
            })

        return jsonify({
            "success": True,
            "payload": {
                "meassage": "Collect User",
                "user_Info": result
            }
        })


@Signin.route('/signup')
class Signup(Resource):
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
            return jsonify({
                "success": False,
                "payload": {
                    "message": e
                }
            })

        db.session.commit()

        return jsonify({
            "success": True,
            "payload": {
                "message": "Sign in OK!"
            }
        })


@Signin.route('/signin')
class Login(Resource):
    def post(self):
        """로그인 API"""
        user_info = request.json['user_info']

        try:
            print('user_info.get(password)', user_info.get('password'))
            print('user_info.get(email)', user_info.get('email'))

            find_user = User.query.filter(
                User.user_email == user_info.get('email')).one()
            isPw = User.checkPw(find_user,
                                user_info.get('password'))

            print('isPw', isPw)
            print('find_user', find_user.user_password)

            if not isPw:
                return jsonify({
                    "success": False,
                    "payload": {
                        "message": f"Fail log in - Invalid password"
                    }
                })
        except Exception as e:
            return jsonify({
                "success": False,
                "payload": {
                    "message": f"Fail log in - {e}"
                }
            })

        return jsonify({
            "success": True,
            "payload": {
                "message": "Log in OK",
                # "user_info": find_user
            }
        })


@Signin.route('/signout')
class Logout(Resource):
    def post(self):
        """로그아웃 API"""
        user_id = session['user_id']
        session.pop(user_id)

        return jsonify({
            "success": True,
            "payload": {
                "message": "Log out OK"
            }
        })
