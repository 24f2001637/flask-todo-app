from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            if User.query.filter_by(username=username).first():
                flash('Username already taken.')
                return redirect(url_for('auth.register'))
        
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Please fill in all fields.', 'danger')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))  
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))