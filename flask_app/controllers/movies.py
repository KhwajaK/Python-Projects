# render_template is used to render the html pages in the templates folder and redirect is used to redirect to a different route in the application 
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')