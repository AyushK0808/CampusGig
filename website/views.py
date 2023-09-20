from flask import Flask,Blueprint,render_template,session,request,redirect,url_for,flash
from flask_login import login_required, current_user
import time
import mysql.connector

db_connection = mysql.connector.connect(
host='localhost',
user='root',
password='mysql',
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

@login_required
@views.route('/recruit', methods=['GET', 'POST'])
def recruit():
    user = current_user.role
    if user == "student":
        return redirect("/")
    user_id = current_user.id
    sql = "SELECT * FROM project WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    jobs = cursor.fetchall()
    
    return render_template("recruit.html", user=current_user,jobs=jobs)

@login_required
@views.route('/recruit/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_recruit(job_id):
    cursor.execute("SELECT * FROM project WHERE id = %s", (job_id,))
    job = cursor.fetchone()

    if job[5] != current_user.id:
        flash("You don't have permission to edit this job listing.", 'danger')
        return redirect(url_for('views.recruit'))

    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        job_budget = request.form.get('job_budget')
        job_skills = request.form.get('job_skills')

        update_query = "UPDATE project SET title=%s, description=%s, budget=%s, skills_required=%s WHERE id=%s"
        values = (job_title, job_description, job_budget, job_skills, job_id)

        cursor.execute(update_query, values)

        flash("Job listing updated successfully.", 'success')
        return redirect(url_for('views.recruit'))

    return render_template("editrecruit.html", user=current_user, job=job)


@login_required
@views.route('/recruitform',methods=['GET','POST'])
def recruitform():
    user = current_user.role
    if user == "student":
        return redirect("/")

    if request.method == 'POST':
        job_title = request.form.get('job_title')
        description = request.form.get('description')
        budget = float(request.form.get('budget'))  # Convert budget to decimal
        skills = ', '.join(request.form.getlist('skills[]'))  # Convert skills list to a comma-separated string
        status = 1  # Convert to 1 for True or 0 for False
        date = time.strftime('%Y-%m-%d')  # Format the date as 'YYYY-MM-DD'
        user_id = current_user.id
        flash('Job listing created successfully', 'success')

        sql = "INSERT INTO project (title, description, budget, skills_required, user_id, date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (job_title, description, budget, skills, user_id, date, status)

        cursor.execute(sql, values)
        db_connection.commit()
        return redirect(url_for('views.recruit'))
    return render_template("recruitform.html")