from flask import Flask
from flask_socketio import SocketIO

import config


socketio = SocketIO(cors_allowed_origins="*")

# 애플리케이션 팩토리
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import main_views, square_goofspiel_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(square_goofspiel_views.bp)

    return app