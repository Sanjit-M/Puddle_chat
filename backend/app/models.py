from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_login import UserMixin
from app import mongo

users_collection = mongo.db.users

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']

    @staticmethod
    def get(user_id):
        user_doc = users_collection.find_one({'_id': ObjectId(user_id)})
        return User(user_doc) if user_doc else None

def create_user(username, password):
    if users_collection.find_one({'username': username}):
        return None, 'Username already exists'
    hashed_password = generate_password_hash(password)
    user_id = users_collection.insert_one({
        'username': username,
        'password': hashed_password
    }).inserted_id
    return users_collection.find_one({'_id': user_id}), None

def validate_login(username, password):
    user_doc = users_collection.find_one({'username': username})
    if user_doc and check_password_hash(user_doc['password'], password):
        return user_doc
    return None

def get_user_count():
    return users_collection.count_documents({})
