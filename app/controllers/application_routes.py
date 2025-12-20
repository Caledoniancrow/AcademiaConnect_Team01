from flask import Blueprint,render_template, request, redirect, url_for, flash, session
from app.models.team_model import TeamDAO
from app.models.application_model import ApplicationDAO

# NOTE: Fixed Blueprint name to match folder structure 'controllers'
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

        # TeamDAO.create_team handles adding the leader to TeamMembers now
        success = TeamDAO.create_team(team_name, leader_id)
        if success:
            flash("Team created successfully! You are now the Team Lead.", "success")
            return redirect(url_for('application_bp.view_my_status'))
        else:
            flash("Failed to create team. Name might be taken.", "danger")

    return render_template('create_team.html')


@application_bp.route('/applications/apply', methods=['POST'])
def apply_to_project():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # 1. Get Data from Form
    team_id = request.form.get('team_id')
    project_id = request.form.get('project_id')
    faculty_id = request.form.get('faculty_id') # <--- NEW: Crucial for FR10
    proposal = request.form.get('proposal')

    # 2. Validation
    if not all([team_id, project_id, faculty_id, proposal]):
        flash("All fields (including Faculty Supervisor) are required", "danger")
        return redirect(request.referrer)

    # 3. Call DAO with the NEW argument structure
    success = ApplicationDAO.apply_to_project(team_id, project_id, faculty_id, proposal)
    
    if success:
        flash("Application submitted to Faculty Supervisor!", "success")
    else:
        flash("Failed. You may have already applied.", "danger")

    return redirect(url_for('application_bp.view_my_status'))


@application_bp.route('/applications/my-status')
def view_my_status():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    # Make sure Mohamed Islam implemented this method in ApplicationDAO!
    # If not, it needs to join TeamMembers to find which team this student belongs to.
    applications = ApplicationDAO.get_applications_by_user(user_id) 
    
    return render_template('view_applications.html', applications=applications)


@application_bp.route('/applications/faculty')
def faculty_dashboard():
    # FIX: Only allow Faculty to see this. Osama had blocked them!
    if session.get('role') != 'Faculty':
        flash("Access denied. Faculty only.", "danger")
        return redirect(url_for('main.index'))

    faculty_id = session.get('user_id')
    applications = ApplicationDAO.get_applications_for_faculty(faculty_id)
    
    return render_template('faculty_dashboard.html', applications=applications)


@application_bp.route('/applications/update-status', methods=['POST'])
def update_application_status():
    # FIX: Role check
    if session.get('role') != 'Faculty':
        return "Unauthorized", 403

    application_id = request.form.get('application_id')
    action = request.form.get('action') # Use 'action' to distinguish buttons

    # Logic: Faculty Approval -> Moves to Industry Review
    if action == 'Approve':
        new_status = 'Pending Industry' # FR11: Industry needs to see it now
        flash("Approved! Forwarded to Industry Partner.", "success")
    elif action == 'Reject':
        new_status = 'Rejected'
        flash("Application Rejected.", "warning")
    else:
        flash("Invalid Action", "danger")
        return redirect(url_for('application_bp.faculty_dashboard'))

    ApplicationDAO