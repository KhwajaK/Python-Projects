from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import movie
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "moviesERD"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fave_movies = []

    @classmethod
    def save_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUE(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"""
        saved_user = connectToMySQL(cls.DB).query_db(query, data)
        print(saved_user)
        return saved_user
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def user_movies(cls, data):
        query = "SELECT * FROM user LEFT JOIN movies ON user.id = movies.user_id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_movies = []
        for row in results:
            user = cls(row)
            movie_data = {
                'id': row['movies.id'],
                'title': row['title'],
                'genre': row['genre'],
                'created_at': row['movies.created_at'],
                'updated_at': row['movies.updated_at'],
                'user_id': row['user_id']
            }
            user.fave_movies = movie.Movie(movie_data)
            all_movies.append(user)
        return all_movies


    @staticmethod
    def validate_new_user(user):
        is_valid = True
        data = {'email': user['email']}
        valid_email = User.get_by_email(data)

        if valid_email:
            flash("Email already in use")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def login_user(user):
        is_valid = True
        data = {'email': user['email']}
        valid_email = User.get_by_email(data)

        if not valid_email:
            flash("Invalid email/password, try again or create an account")
            is_valid = False
        elif not bcrypt.check_password_hash(valid_email.password, user['password']) :
            flash("Invalid email/password, try again or create an account")
            is_valid = False
        if len(user['email']) <1 and len(user['password']) < 1:
            flash("Please enter your email and password")
            is_valid = False
        return is_valid