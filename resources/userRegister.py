import sqlite3
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from models.usermodel import userModel
from werkzeug.security import safe_str_cmp


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                          type=str,
                          required=True,
                          help="username cannot be empty")
_user_parser.add_argument("password",
                          type=str,
                          required=True,
                          help="password cannot be empty")


class user_register(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if userModel.find_by_username(data['username']):
            return {"Registration": "Username already exist"},400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES(NULL,?,?)", (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"Registeration": "Successful"}, 201


class user_login(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = userModel.find_by_username(data['username'])
        if user and safe_str_cmp(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        return {"Login": "Wrong Credentials"}

