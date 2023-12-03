from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_query = User.query.filter_by(username=username).first()
        if user_query:
            if password == user_query.password:
                login_user(user_query, remember=True)
                flash('Login successful!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='danger')
        else:
            flash('Username not found', category='danger')

    return render_template('login.html', user=current_user)

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_query = User.query.filter_by(username=username).first()
        if user_query:
            flash('Username already exists.', category='danger')
        elif len(password) < 8:
            flash('Password must be 8 or more characters long.', category='danger')
        elif password != confirm_password:
            flash('Passwords do not match.', category='danger')
        else:
            new_user = User(
            username=username,
            password=password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html', user=current_user)