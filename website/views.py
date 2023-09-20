from flask import Flask,Blueprint,render_template,session,request,redirect,url_for,flash
from flask_login import login_required, current_user
import time
import mysql.connector

db_connection = mysql.connector.connect(
host='localhost',
user='root',
password='root',
database='hackbattle'
)
cursor=db_connection.cursor()
cursor = db_connection.cursor(buffered=True)

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
    role=current_user.role
    cursor.execute('SELECT skill_name FROM skill')
    skills_data = cursor.fetchall()
    return render_template("profile.html",user=current_user,username=username,user_id=user_id,email=email,role=role,skills=skills_data)

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

    user_id = current_user.id
    sql = "SELECT * FROM project WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    jobs = cursor.fetchall()
    
    return render_template("recruit.html", user=current_user,jobs=jobs)

@login_required
@views.route('/collab', methods=['GET', 'POST'])
def collab():
    user = current_user.role
    user_id = current_user.id
    sql = "SELECT * FROM project WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    jobs = cursor.fetchall()
    
    return render_template("collab.html", user=current_user,jobs=jobs)

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
@views.route('/recruit/delete/<int:job_id>', methods=['GET', 'POST'])
def delete_recruit(job_id):
    cursor.execute("SELECT * FROM project WHERE id = %s", (job_id,))
    job = cursor.fetchone()

    if job[5] != current_user.id:
        flash("You don't have permission to edit this job listing.", 'danger')
        return redirect(url_for('views.recruit'))
    
    delete_query = "DELETE FROM project WHERE id = %s"
    cursor.execute(delete_query, (job_id,))
    return redirect(url_for('views.recruit'))

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
    return render_template("recruitform.html",user=current_user)

@login_required
@views.route('/opportunities',methods=['GET','POST'])
def opportunities():
    sql = "SELECT * FROM project"
    cursor.execute(sql)
    jobs = cursor.fetchall()
    for job in jobs:
        pass
    return render_template("opportunities.html",jobs=jobs,user = current_user)

@login_required
@views.route('/application/<int:job_id>',methods=['GET','POST'])
def application(job_id):
    user_id = current_user.id
    sql = "SELECT * FROM application WHERE jobid = %s AND user_id = %s"
    values = (job_id, user_id)
    cursor.execute(sql, values)
    record = cursor.fetchone()
    if record:
        return redirect(url_for('views.opportunities'))
    if request.method == 'POST':
        timeframe = request.form['timeframe']
        price_quote = request.form['price_quote']
        remarks = request.form['remarks']
        sql = "INSERT INTO application (jobid, quote, remarks, date, user_id) VALUES (%s, %s, %s, %s, %s)"
        values = (job_id, price_quote, remarks, timeframe, user_id)
        cursor.execute(sql, values)
        db_connection.commit()
        return redirect(url_for('views.myapplications'))

    sql = "SELECT * FROM project WHERE id = %s"
    cursor.execute(sql, (job_id,))
    job = cursor.fetchone()
    return render_template("application.html",job=job,user = current_user)

@login_required
@views.route('/collabform',methods=['GET','POST'])
def collabform():
    user = current_user.role

    if request.method == 'POST':
        job_title = request.form.get('job_title')
        description = request.form.get('description')
        budget = 0  # Convert budget to decimal
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
    return render_template("collabform.html")

@login_required
@views.route('/myapplications',methods=['GET','POST'])
def myapplications():
    user_id = current_user.id
    sql = "SELECT * FROM application WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    applications = cursor.fetchall()
    return render_template("myapplications.html",applications=applications,user = current_user)
