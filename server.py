from flask_app import app

from flask_app.controllers import users, movies
if __name__=='__main__':
    app.run(Port=8000, debug=True)