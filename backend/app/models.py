from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import mongo
from datetime import datetime

users_collection = mongo.db.users
messages_collection = mongo.db.messages

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = user_doc['username']
        self.username = user_doc['username']

    @staticmethod
    def get(username):
        user_doc = users_collection.find_one({'username': username})
        return User(user_doc) if user_doc else None

def create_user(username, password):
    if users_collection.find_one({'username': username}):
        return None, 'Username already exists'
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        'username': username,
        'password': hashed_password
    })
    return users_collection.find_one({'username': username}), None

def validate_login(username, password):
    user_doc = users_collection.find_one({'username': username})
    if user_doc and check_password_hash(user_doc['password'], password):
        return user_doc
    return None

def get_user_count():
    return users_collection.count_documents({})

class Message:
    def __init__(self, message_doc):
        self.sender = message_doc['sender']
        self.receiver = message_doc['receiver']
        self.content = message_doc['content']
        self.timestamp = message_doc['timestamp']

    @staticmethod
    def create_message(sender, receiver, content):
        message_data = {
            'sender': sender,
            'receiver': receiver,
            'content': content,
            'timestamp': datetime.now()
        }
        message_id = messages_collection.insert_one(message_data).inserted_id
        return messages_collection.find_one({'_id': message_id})

    @staticmethod
    def get_messages_between_users(user1, user2, limit=20):
        return messages_collection.find({
            '$or': [
                {'sender': user1, 'receiver': user2},
                {'sender': user2, 'receiver': user1}
            ]
        }).sort('timestamp', 1).limit(limit)
