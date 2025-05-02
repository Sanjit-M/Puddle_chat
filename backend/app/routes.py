from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager
from app.models import User, create_user, validate_login, get_user_count, Message
import requests

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def build_prompt_from_history(messages, new_user_message):
    prompt = ""
    # Convert cursor to list so we can reverse it
    messages_list = list(messages)
    for msg in reversed(messages_list):
        sender = "User" if msg['sender'] == 'user' else "Assistant"
        prompt += f"{sender}: {msg['content']}\n"
    prompt += f"User: {new_user_message}\nAssistant:"
    return prompt

def get_llm_response(username, user_message):
    history = Message.get_conversation(username, limit=10)
    prompt = build_prompt_from_history(history, user_message)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=15
        )
        return response.json().get("response", "Internal Server Error: Go touch grass")
    except Exception as e:
        return f"LLM error: {str(e)}"


@main.route('/')
def home():
    return 'Flask app connected to Ollama LLM is running!'

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
    
@main.route('/check-auth')
@login_required
def check_auth():
    return jsonify({'authenticated': True}), 200

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    content = request.json.get('content')
    username = current_user.username

    if not content:
        return jsonify({'message': 'Message content is required'}), 400

    # Save user's message
    Message.save_message(username, 'user', content)

    # Get LLM response based on history
    llm_reply = get_llm_response(username, content)

    # Save LLM's response
    Message.save_message(username, 'llm', llm_reply)

    return jsonify({'response': llm_reply}), 200

@main.route('/get_conversation', methods=['GET'])
@login_required
def get_conversation():
    username = current_user.username
    messages = Message.get_conversation(username)
    formatted = [
        {
            'sender': msg['sender'],
            'content': msg['content'],
            'timestamp': msg['timestamp']
        } for msg in messages
    ][::-1]  # reverse to chronological order

    return jsonify({'messages': formatted}), 200

@main.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    username = current_user.username
    deleted_count = Message.clear_conversation(username)

    return jsonify({
        'message': f'Conversation history cleared. {deleted_count} messages deleted.'
    }), 200
