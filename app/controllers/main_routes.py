from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.project_model import ProjectDAO



main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

  
    user_role = session.get('role')
    projects_list = []

  
    if user_role == 'Student' or user_role == 'Faculty': 
        projects_list = ProjectDAO.get_all_projects()
      
    return render_template('dashboard.html', projects=projects_list, role=user_role)




@main_bp.route('/create_project', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

  

    title = request.form.get('title')
    description = request.form.get('description')
    industry_id = session['user_id']

  
    ProjectDAO.create_project(title, description, industry_id)

  
    return redirect(url_for('main.dashboard'))
