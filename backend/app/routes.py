from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager
from app.models import User, create_user, validate_login, get_user_count, Message

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(username):
    return User.get(username)

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

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    receiver = data.get('receiver')
    content = data.get('content')

    if not receiver or not content:
        return jsonify({'message': 'Receiver and content are required'}), 400

    message = Message.create_message(current_user.username, receiver, content)

    return jsonify({
        'message': 'Message sent successfully',
        'data': {
            'sender': message['sender'],
            'receiver': message['receiver'],
            'content': message['content'],
            'timestamp': message['timestamp']
        }
    }), 201

@main.route('/get_messages', methods=['GET'])
@login_required
def get_messages():
    other_user = request.args.get('other_user')

    if not other_user:
        return jsonify({'message': 'Other user is required'}), 400

    messages = Message.get_messages_between_users(current_user.username, other_user)

    formatted_messages = [
        {
            'sender': message['sender'],
            'receiver': message['receiver'],
            'content': message['content'],
            'timestamp': message['timestamp']
        }
        for message in messages
    ]

    return jsonify({'messages': formatted_messages}), 200
