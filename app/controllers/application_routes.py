from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.team_model import TeamDAO
from app.models.application_model import ApplicationDAO
from app.models.project_model import ProjectDAO

application_bp = Blueprint('application_bp', __name__)

@application_bp.route('/teams/create', methods=['GET', 'POST'])
def create_team():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        team_name = request.form.get('team_name')
        leader_id = session.get('user_id')

        if not team_name:
            flash("Team name is required", "danger")
            return redirect(url_for('application_bp.create_team'))

        team_id = TeamDAO.create_team(team_name, leader_id)
        if team_id:
            flash("Team created successfully! You are now the Team Lead.", "success")
            return redirect(url_for('application_bp.view_teams'))
        else:
            flash("Failed to create team. Name might be taken.", "danger")

    return render_template('create_team.html')


@application_bp.route('/teams/my-teams')
def view_teams():
    """View all teams the current user is part of"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    teams = TeamDAO.get_teams_by_member(user_id)
    
    return render_template('my_teams.html', teams=teams)


@application_bp.route('/teams/<int:team_id>/manage')
def manage_team(team_id):
    """Manage a specific team (view members, add/remove)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    team_details = TeamDAO.get_team_details(team_id)
    
    if not team_details:
        flash("Team not found", "danger")
        return redirect(url_for('application_bp.view_teams'))
    
    # Check if user is a member of this team
    members = TeamDAO.get_team_members(team_id)
    is_member = any(member[0] == user_id for member in members)
    
    if not is_member:
        flash("You are not a member of this team", "danger")
        return redirect(url_for('application_bp.view_teams'))
    
    is_leader = team_details[2] == user_id
    
    return render_template('manage_team.html', 
                         team=team_details, 
                         members=members, 
                         is_leader=is_leader)


@application_bp.route('/teams/<int:team_id>/add-member', methods=['POST'])
def add_team_member(team_id):
    """Add a member to the team by email"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    email = request.form.get('email')
    user_id = session.get('user_id')
    
    result = TeamDAO.add_member_by_email(team_id, email, user_id)
    
    if result == "Success":
        flash("Member added successfully!", "success")
    else:
        flash(result, "danger")
    
    return redirect(url_for('application_bp.manage_team', team_id=team_id))


@application_bp.route('/teams/<int:team_id>/remove-member/<int:student_id>', methods=['POST'])
def remove_team_member(team_id, student_id):
    """Remove a member from the team"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    
    result = TeamDAO.remove_member(team_id, student_id, user_id)
    
    if result == "Success":
        flash("Member removed successfully!", "success")
    else:
        flash(result, "danger")
    
    return redirect(url_for('application_bp.manage_team', team_id=team_id))


@application_bp.route('/teams/<int:team_id>/delete', methods=['POST'])
def delete_team(team_id):
    """Delete a team (only leader can do this)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    result = TeamDAO.delete_team(team_id, user_id)
    
    if result == "Success":
        flash("Team deleted successfully!", "success")
    else:
        flash(result, "danger")
    
    return redirect(url_for('application_bp.view_teams'))


@application_bp.route('/projects/<int:project_id>/apply')
def apply_form(project_id):
    """Show application form for a specific project"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('role') != 'Student':
        flash("Only students can apply to projects", "danger")
        return redirect(url_for('main.dashboard'))
    
    # Get project details
    project = ProjectDAO.get_project_by_id(project_id)
    if not project:
        flash("Project not found", "danger")
        return redirect(url_for('main.dashboard'))
    
    # Get user's teams
    user_id = session.get('user_id')
    teams = TeamDAO.get_teams_by_member(user_id)
    
    # Get team member counts
    team_member_counts = {}
    for team in teams:
        members = TeamDAO.get_team_members(team[0])
        team_member_counts[team[0]] = len(members)
    
    return render_template('apply_form.html', 
                         project=project, 
                         teams=teams,
                         team_member_counts=team_member_counts)


@application_bp.route('/applications/apply', methods=['POST'])
def apply_to_project():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    team_id = request.form.get('team_id')
    project_id = request.form.get('project_id')
    faculty_id = request.form.get('faculty_id')
    proposal = request.form.get('proposal')

    if not all([team_id, project_id, faculty_id, proposal]):
        flash("All fields are required", "danger")
        return redirect(request.referrer)

    success = ApplicationDAO.apply_to_project(team_id, project_id, faculty_id, proposal)
    
    if success:
        flash("Application submitted for review!", "success")
    else:
        flash("Failed. You may have already applied to this project.", "danger")

    return redirect(url_for('application_bp.view_my_status'))


@application_bp.route('/applications/my-status')
def view_my_status():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    applications = ApplicationDAO.get_applications_by_user(user_id) 
    
    return render_template('view_applications.html', applications=applications)


@application_bp.route('/applications/faculty')
def faculty_dashboard():
    if session.get('role') != 'Faculty':
        flash("Access denied. Faculty only.", "danger")
        return redirect(url_for('main.index'))

    faculty_id = session.get('user_id')
    applications = ApplicationDAO.get_applications_for_faculty(faculty_id)
    
    return render_template('faculty_dashboard.html', applications=applications)


@application_bp.route('/applications/industry')
def industry_dashboard():
    if session.get('role') != 'Industry':
        flash("Access denied. Industry only.", "danger")
        return redirect(url_for('main.index'))

    industry_id = session.get('user_id')
    applications = ApplicationDAO.get_applications_for_industry(industry_id)
    
    return render_template('industry_applications.html', applications=applications)


@application_bp.route('/applications/<int:app_id>/details')
def application_details(app_id):
    """View detailed info about an application"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    application = ApplicationDAO.get_application_details(app_id)
    
    if not application:
        flash("Application not found", "danger")
        return redirect(url_for('main.dashboard'))
    
    # Get team members
    team_id = application[4]
    team_members = TeamDAO.get_team_members(team_id)
    
    return render_template('application_details.html', 
                         application=application,
                         team_members=team_members)


@application_bp.route('/applications/update-status', methods=['POST'])
def update_application_status():
    """Faculty or Industry can approve/reject applications"""
    if session.get('role') not in ['Faculty', 'Industry']:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.dashboard'))

    application_id = request.form.get('application_id')
    action = request.form.get('action')
    role = session.get('role')

    if action == 'Approve':
        if role == 'Faculty':
            new_status = 'Faculty Approved'
            flash("Approved! Forwarded to Industry Partner.", "success")
        else:  # Industry
            new_status = 'Approved'
            flash("Application approved! Team can now start work.", "success")
    elif action == 'Reject':
        new_status = 'Rejected'
        flash("Application Rejected.", "warning")
    else:
        flash("Invalid Action", "danger")
        return redirect(request.referrer)

    ApplicationDAO.update_status(application_id, new_status)
    return redirect(request.referrer)