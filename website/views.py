from flask import Flask,Blueprint,render_template,session,request,redirect,url_for,flash
from flask_login import login_required, current_user

import mysql.connector
db_connection = mysql.connector.connect(
host='localhost',
user='root',
password='root',
database='hackbattle'
)
cursor=db_connection.cursor()

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html",user=current_user)

@login_required
@views.route('/profile')
def profile():
    user_id = current_user.id
    username = current_user.username
    email = current_user.email
    return f'Hello User ID: {user_id}, Username: {username}, Email: {email}'

@login_required
@views.route('/editprofile',methods=['GET','POST'])
def edit_profile():
    cursor.execute('SELECT skill_name FROM skill')
    skills_data = cursor.fetchall()
    if request.method=='GET':
        selected_skills = request.form.getlist('skills[]')
    print(selected_skills)
    return render_template("editprofile.html",user=current_user,skills=skills_data)