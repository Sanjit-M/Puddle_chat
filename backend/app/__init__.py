from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

socketio = SocketIO()
login_manager = LoginManager()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/chat_db'  # or MongoDB Atlas URI

    mongo.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
