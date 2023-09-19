from flask import Flask 
from os import path
from flask_mysqldb import MySQL
def create_app():
    from .auth import auth
    from .views import views
    app = Flask(__name__)

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'hackbattle'
    app.secret_key = 'your secret key'
    mysql = MySQL(app)


    return app 
