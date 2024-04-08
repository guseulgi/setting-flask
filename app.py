from flask import Flask
from flask_session import Session
from flask_restx import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from config import AppConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()


def create_app():
    app = Flask(__name__)

    app.config.from_object(AppConfig)

    api = Api(app,
              version='1.0',
              title="Moncolle API Server",
              description="Testing",
              license="MIT")

    Session(app)
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    bcrypt.init_app(app)

    # Models
    from models.users import User

    with app.app_context():
        db.create_all()

    # Route
    from routes.signin import Signin

    api.add_namespace(Signin, '/api/user')

    return app


if __name__ == '__main__':
    app = create_app()
    app.config.update(SESSION_COOKIE_SAMESITE="None",
                      SESSION_COOKIE_SECURE=True)
    app.run(debug=True)
