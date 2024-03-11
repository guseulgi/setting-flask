from flask_restx import Resource, Namespace

Signin = Namespace('Signin')

# 로그인 API

# 로그아웃 API


@Signin.route('/signup')
class Signup(Resource):
    """ 회원가입 """

    def post(self):
        return
