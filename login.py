from werkzeug.security import safe_str_cmp
from models.usermodel import userModel


def authenticate(username, password):
    user = userModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_identity = payload['identity']
    return userModel.find_by_id(user_identity)
