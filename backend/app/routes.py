from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login_manager

main = Blueprint('main', __name__)
users_collection = mongo.db.users

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']

@login_manager.user_loader
def load_user(user_id):
    user_doc = users_collection.find_one({'_id': mongo.db.ObjectId(user_id)})
    return User(user_doc) if user_doc else None

@main.route('/')
def home():
    return 'Flask app with MongoDB Atlas is running!'

@main.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    user_id = users_collection.insert_one({'username': username, 'password': hashed_password}).inserted_id
    user = users_collection.find_one({'_id': user_id})
    login_user(User(user))
    return jsonify({'message': 'User registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401

    login_user(User(user))
    return jsonify({'message': 'Logged in successfully'}), 200

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

@main.route('/test-db')
def test_db():
    try:
        user_count = users_collection.count_documents({})
        return jsonify({'message': f'Database connected. {user_count} users found.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
