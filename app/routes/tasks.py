from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__)
@task_bp.route('/')
def view_tasks():
    if 'user' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task title cannot be empty.', 'danger')
    
    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Completed'
        else:
            task.status = 'Pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found.', 'danger')

    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/clear', methods=['POST'])
def clear_tasks():
    if 'user' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared successfully!', 'success')
    
    return redirect(url_for('tasks.view_tasks'))
