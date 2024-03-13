from Flask import Flask
from flask_session import Session
from flask_restx import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from routes.signin import Signin

from config import AppConfig

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config.from_object(AppConfig)

    api = Api(app,
              version='1.0',
              title="Moncolle API Server",
              description="Testing",
              license="MIT")

    Session(app)
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    api.add_namespace(Signin, '/api/signin')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
