from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db
import hashlib

admin_bp = Blueprint('admin_bp', __name__)

# --- SECURITY DECORATOR (Optional but clean) ---
def login_required_admin():
    if 'user_id' not in session:
        return False
    if session.get('role') != 'Admin':
        return False
    return True

@admin_bp.route('/admin/dashboard')
def dashboard():
    if not login_required_admin():
        flash("Access Denied. Admins Only.", "danger")
        return redirect(url_for('auth.login'))

    conn = get_db()
    cursor = conn.cursor()

    # 1. Fetch System Stats
    cursor.execute("SELECT COUNT(*) FROM Users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Projects")
    project_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Teams")
    team_count = cursor.fetchone()[0]

    # 2. Fetch Recent Users (for the table)
    cursor.execute("SELECT UserID, FullName, Email, Role FROM Users")
    users = cursor.fetchall()

    return render_template('admin_dashboard.html', 
                           user_count=user_count, 
                           project_count=project_count, 
                           team_count=team_count,
                           users=users)

@admin_bp.route('/admin/create-user', methods=['GET', 'POST'])
def create_user():
    """Allows Admin to manually create Faculty or Industry accounts"""
    if not login_required_admin():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # Faculty, Industry, or Admin

        if not all([name, email, password, role]):
            flash("All fields are required", "danger")
            return redirect(url_for('admin_bp.create_user'))

        # Hash Password
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Users (FullName, Email, PasswordHash, Role)
                VALUES (?, ?, ?, ?)
            """, (name, email, hashed_pw, role))
            conn.commit()
            flash(f"User {name} ({role}) created successfully!", "success")
            return redirect(url_for('admin_bp.dashboard'))
        except Exception as e:
            flash("Error creating user. Email might be taken.", "danger")
    
    return render_template('admin_create_user.html')