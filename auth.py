from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth_bp', __name__)

# Hardcoded admin credentials
ADMIN_CREDENTIALS = {'username': 'admin', 'password': 'admin123'}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['admin'] = username
            return redirect(url_for('student_bp.dashboard'))  # ✅ Go to dashboard after login
        flash('❌ Invalid credentials. Please try again.')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('admin', None)
    flash("✅ Logged out successfully.")
    return redirect(url_for('auth_bp.login'))
