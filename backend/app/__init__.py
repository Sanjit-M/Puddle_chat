import os
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv

socketio = SocketIO()
mongo = PyMongo()
login_manager = LoginManager()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    mongo_user = os.getenv('MONGO_USER')
    mongo_password = os.getenv('MONGO_PASSWORD')
    mongo_cluster = os.getenv('MONGO_CLUSTER')
    mongo_db = os.getenv('MONGO_DB_NAME')

    app.config['MONGO_URI'] = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/{mongo_db}?retryWrites=true&w=majority"

    mongo.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    CORS(app, supports_credentials=True)  # Allow cross-origin requests with cookies

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
