from flask import request, jsonify
from flask_restx import Resource, Namespace

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


@Signin.route('/signin')
class Logout(Resource):
    def post(self):
        """로그인"""
        return


@Signin.route('/signout')
class Logout(Resource):
    def post(self):
        """로그아웃"""
        return


@Signin.route('/signup')
class Signup(Resource):
    def post(self):
        """ 회원가입 """
        return
