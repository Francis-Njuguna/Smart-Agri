"""
Admin dashboard for Smart Agriculture System
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from utils.db import execute_query
from models.admin import AdminUser, create_admin_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminUser.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin/farmers')
@login_required
def farmers():
    query = "SELECT * FROM farmers ORDER BY created_at DESC"
    farmers = execute_query(query)
    return render_template('farmers.html', farmers=farmers)

@app.route('/admin/crops')
@login_required
def crops():
    query = "SELECT * FROM crops ORDER BY name"
    crops = execute_query(query)
    return render_template('crops.html', crops=crops)

@app.route('/admin/locations')
@login_required
def locations():
    query = "SELECT * FROM locations ORDER BY name"
    locations = execute_query(query)
    return render_template('locations.html', locations=locations)

if __name__ == '__main__':
    # Create default admin user if none exists
    create_admin_user('admin', 'admin123')
    app.run(port=5001, debug=True) 