from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()


def create_app():
    from .auth import auth
    from .views import views
    app = Flask(__name__)

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    app.config['SECRET_KEY'] = 'NoIdontwantthat'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mysql@localhost/hackbattle"
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app 

def db_connect():
    import mysql.connector
    db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysql',
    database='hackbattle'
    )
    return db_connection.cursor()