from flask import Blueprint,render_template, request, redirect, url_for, flash, session
from app.models.milestone_model import MilestoneDAO

milestone_bp = Blueprint('milestone_bp', __name__)

@milestone_bp.route('/projects/<int:project_id>/milestones')
def view_milestones(project_id):
    """
    Shows the Milestones for a specific project.
    Visible to: Team Members (Student), Supervisor (Faculty), and Owner (Industry).
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # 1. Fetch Milestones
    milestones = MilestoneDAO.get_project_milestones(project_id)
    
    # 2. Determine Permissions (to show/hide buttons in HTML)
    user_role = session.get('role')
    
    return render_template('project_milestones.html', 
                           milestones=milestones, 
                           project_id=project_id, 
                           user_role=user_role)

@milestone_bp.route('/milestones/submit', methods=['POST'])
def submit_milestone():
    """FR12: Student submits a link"""
    if session.get('role') != 'Student':
        flash("Only students can submit work.", "danger")
        return redirect(request.referrer)

    milestone_id = request.form.get('milestone_id')
    submission_link = request.form.get('submission_link')

    if MilestoneDAO.submit_work(milestone_id, submission_link):
        flash("Work submitted successfully!", "success")
    else:
        flash("Error submitting work.", "danger")

    return redirect(request.referrer)

@milestone_bp.route('/milestones/approve', methods=['POST'])
def approve_milestone():
    """FR13: Faculty or Industry approves the work"""
    if session.get('role') not in ['Faculty', 'Industry']:
        flash("Unauthorized", "danger")
        return redirect(request.referrer)

    milestone_id = request.form.get('milestone_id')
    
    # Simple approval (sets status to 'Completed')
    # Note: For FR14 (Final Grading), you might want a separate route or check if it's the last milestone.
    if MilestoneDAO.grade_milestone(milestone_id, 100): # Auto-grade 100 for approval, or add input for grade
        flash("Milestone approved!", "success")
    else:
        flash("Error approving milestone.", "danger")

    return redirect(request.referrer)
