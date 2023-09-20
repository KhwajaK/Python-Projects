from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Movie:
    DB = "moviesERD"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @staticmethod
    def validate(movie):
        is_valid = True
        if len(movie['title']) < 2:
            flash("Title must be at least 2 characters")
            is_valid = False
        if len(movie['genre']) < 2:
            flash("Genre must be at least 2 characters")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_movies(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(cls.DB).query_db(query)
        movies = []
        for x in results:
            movies.append(cls(x))
        return movies

    @classmethod
    def save_movie(cls, data):
        query = """INSERT INTO movies (title, genre, created_at, updated_at) VALUE(%(title)s, %(genre)s, NOW(), NOW());"""
        saved_movie = connectToMySQL(cls.DB).query_db(query, data)
        print(saved_movie)
        return saved_movie
    
    @classmethod
    def view_one_movie(cls, data):
        query = "SELECT * FROM movies WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update_movie(cls, data):
        query = "UPDATE movies SET title = %(title)s, genre = %(genre)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_movie(cls, data):
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def user_fave_movies(cls,data):
        query = "SELECT * FROM movies LEFT JOIN user ON movies.user_id = user.id WHERE movie.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        for x in results:
            movie = cls(x)
            user_data = {
                'id': x['user.id'],
                'first_name': x['first_name'],
                'last_name': x['last_name'],
                'email': x['email'],
                'password': x['password'],
                'created_at': x['user.created_at'],
                'updated_at': x['user.updated_at']
            }
            movie.user = user.User(user_data)
        return movie