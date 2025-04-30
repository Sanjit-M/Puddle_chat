from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app import login_manager
from app.models import User, create_user, validate_login, get_user_count

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@main.route('/')
def home():
    return 'Flask app with MongoDB Atlas is running!'

@main.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_doc, error = create_user(username, password)
    if error:
        return jsonify({'message': error}), 409

    login_user(User(user_doc))
    return jsonify({'message': 'User registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_doc = validate_login(username, password)
    if not user_doc:
        return jsonify({'message': 'Invalid username or password'}), 401

    login_user(User(user_doc))
    return jsonify({'message': 'Logged in successfully'}), 200

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

@main.route('/test-db')
def test_db():
    try:
        count = get_user_count()
        return jsonify({'message': f'Database connected. {count} users found.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
