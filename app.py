from flask import Flask
from flask_session import Session
from flask_restx import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from config import AppConfig

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True)
    app.config.from_object(AppConfig)
    Session(app)
    db.init_app(app)
    bcrypt.init_app(app)

    api = Api(app,
              version='1.0',
              title="Moncolle API Server",
              description="Testing",
              license="MIT")

    # Models
    from models.users import User

    with app.app_context():
        db.create_all()

    # Route
    from routes.signin import Signin

    api.add_namespace(Signin, '/api/users')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
