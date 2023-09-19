from flask import Flask,Blueprint,render_template,session,request,redirect,url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('<h1>Test</h1>')



