from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import hashlib
from app.models.user_model import UserDAO 



auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_row = UserDAO.get_user_by_email(email)

      
        if user_row:
            stored_hash = user_row[3] 
            input_hash = hashlib.sha256(password.encode()).hexdigest()

          
            if input_hash == stored_hash:
                session['user_id'] = user_row[0]
                session['username'] = user_row[1]
                session['role'] = user_row[4]
                return redirect(url_for('main.dashboard'))
            else:
                flash('Incorrect Password.', 'danger')
              
        else:
            flash('Email not found.', 'danger')
          

    return render_template('login.html')




@auth_bp.route('/register', methods=['GET', 'POST'])


def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        success = UserDAO.create_user(username, email, password, role)

      
        if success:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('auth.login'))
          
        else:
            flash('Registration failed. Email might be taken.', 'danger')
          

    return render_template('register.html')





@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
