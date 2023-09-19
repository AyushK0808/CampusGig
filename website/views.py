from flask import Flask,Blueprint,render_template,session,request,redirect,url_for,flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html",user=current_user)

@login_required
@views.route('/profile')
def profile():
    
    return render_template("profile.html",user=current_user)