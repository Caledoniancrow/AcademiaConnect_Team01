from flask import render_template, request, redirect, url_for, session, flash
from app.controllers import main_bp 
from app.models.project_model import ProjectDAO

# --- THIS WAS MISSING ---
@main_bp.route('/')
def index():
    # When user visits localhost:5000/, jump to /login
    return redirect(url_for('auth.login'))
# ------------------------

@main_bp.route('/dashboard')
def dashboard():
    # 1. Security Check
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_role = session.get('role')
    projects_list = []
    
    # 2. Logic: Fetch projects for Students/Faculty
    if user_role == 'Student' or user_role == 'Faculty':
        projects_list = ProjectDAO.get_all_projects()
        
    # 3. Render
    return render_template('dashboard.html', projects=projects_list, role=user_role)

@main_bp.route('/create_project', methods=['POST'])
def create_project():
    # 1. Security Check
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    # 2. Get Data
    title = request.form.get('title')
    description = request.form.get('description')
    industry_id = session['user_id']
    
    # 3. Call Model
    ProjectDAO.create_project(title, description, industry_id)
    
    # 4. Redirect
    return redirect(url_for('main.dashboard'))