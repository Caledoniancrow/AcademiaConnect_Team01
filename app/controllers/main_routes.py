from flask import render_template, request, redirect, url_for, session, flash
from app.controllers import main_bp 
from app.models.project_model import ProjectDAO


@main_bp.route('/')
def index():
    """
    Landing page - shows home.html if not logged in
    Redirects to dashboard if already logged in
    """
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    
    return render_template('home.html')


@main_bp.route('/dashboard')
def dashboard():
    """
    Role-based dashboard view
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_role = session.get('role')
    projects_list = []
    
    # Fetch projects based on role
    if user_role in ['Student', 'Faculty', 'Industry']:
        projects_list = ProjectDAO.get_all_projects()
    
    return render_template('dashboard.html', projects=projects_list, role=user_role)


@main_bp.route('/create_project', methods=['POST'])
def create_project():
    """
    Industry partners can create new projects
    """
    if 'user_id' not in session:
        flash('You must be logged in to create a project', 'danger')
        return redirect(url_for('auth.login'))
    
    if session.get('role') != 'Industry':
        flash('Only Industry partners can create projects', 'danger')
        return redirect(url_for('main.dashboard'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    industry_id = session['user_id']
    
    if not title or not description:
        flash('Project title and description are required', 'danger')
        return redirect(url_for('main.dashboard'))
    
    success = ProjectDAO.create_project(title, description, industry_id)
    
    if success:
        flash('Project submitted successfully! It will be reviewed by administrators.', 'success')
    else:
        flash('Failed to create project. Please try again.', 'danger')
    
    return redirect(url_for('main.dashboard'))