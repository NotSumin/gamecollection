from flask import Flask
from flask_socketio import SocketIO

import config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from .views import main_views, square_goofspiel_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(square_goofspiel_views.bp)

    socketio.init_app(app, cors_allowed_origins="*")

    return app