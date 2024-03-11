from Flask import Flask
from flask_session import Session
from flask_restx import Api
from flask_cors import CORS

from config import AppConfig


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

    return api


if __name__ == '__main__':
    app = create_app()
    app.run()
