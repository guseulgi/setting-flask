from flask import request, jsonify, session
from flask_restx import Resource, Namespace

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

        result = User.query.filter(User.user_id == user_id).one()
        return jsonify({
            "success": True,
            "payload": {
                "meassage": "Collect User",
                "userInfo": result
            }
        })


@Signin.route('/signup')
class Signup(Resource):
    def post(self):
        """ 회원가입 API """
        request_result = request.json['userInfo']
        request_nickname = request_result.get('nickname')
        request_email = request_result.get('email')
        request_password = request_result.get('password')

        user = User(nickname=request_nickname,
                    email=request_email, password=request_password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "payload": {
                "message": "Sign In OK!"
            }
        })


@Signin.route('/signin')
class Logout(Resource):
    def post(self):
        """로그인 API"""
        return


@Signin.route('/signout')
class Logout(Resource):
    def post(self):
        """로그아웃 API"""
        return
