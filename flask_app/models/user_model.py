from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re #regex101.com
# import time (this is for dates/time)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "user_registration"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE 
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s )
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    # READ
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        # go through length of results and search for email
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    # DELETE
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM users 
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return results

    # REGISTER VALIDATIONS
    @staticmethod
    def validate_registration(user):
        is_valid = True
        # checking database to make sure they're not already registered 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash ("Email already registered. Please log in!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format!', "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash ('First Name must be at least 2 characters.', "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash ('Last Name must be at least 2 characters.', "register")
            is_valid = False
        if len(user['password']) < 8:
            flash ('Password must be at least 8 characters.', "register")
            is_valid = False
        # compare password
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid
