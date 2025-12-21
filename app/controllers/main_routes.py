from flask import render_template, request, redirect, url_for, session, flash
from app.controllers import main_bp 
from app.models.project_model import ProjectDAO


@main_bp.route('/')
def index():
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
    
    if user_role == 'Industry':
        # Shows ONLY projects created by this Industry Partner
        projects_list = ProjectDAO.get_projects_by_industry(session['user_id'])
    elif user_role in ['Student', 'Faculty']:
        # Shows ALL projects
        projects_list = ProjectDAO.get_all_projects()
    
    return render_template('dashboard.html', projects=projects_list, role=user_role)


@main_bp.route('/create_project', methods=['POST'])
def create_project():
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
        flash('Project created successfully!', 'success')
    else:
        flash('Failed to create project. Please try again.', 'danger')
    
    return redirect(url_for('main.dashboard'))


@main_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    """Delete a project (only owner can delete)"""
    if 'user_id' not in session:
        flash('You must be logged in', 'danger')
        return redirect(url_for('auth.login'))
    
    if session.get('role') != 'Industry':
        flash('Only Industry partners can delete projects', 'danger')
        return redirect(url_for('main.dashboard'))
    
    industry_id = session['user_id']
    result = ProjectDAO.delete_project(project_id, industry_id)
    
    if result == "Success":
        flash('Project deleted successfully!', 'success')
    else:
        flash(result, 'danger')
    
    return redirect(url_for('main.dashboard'))