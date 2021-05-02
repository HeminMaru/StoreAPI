import sqlite3
from flask_restful import Resource, reqparse
from models.usermodel import userModel


class user_register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="username cannot be empty")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="password cannot be empty")

    def post(self):
        data = user_register.parser.parse_args()
        if userModel.find_by_username(data['username']):
            return {"Registration": "Username already exist"},400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES(NULL,?,?)", (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"Registeration": "Successful"}, 201


