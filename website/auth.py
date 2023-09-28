from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        twitter_tag = request.form.get('twitter_tag')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(twitter_tag=twitter_tag).first()
        if user:
            flash('User already exists!', category='error')
        elif len(twitter_tag) == 0:
            flash('Invalid Twitter name.', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(twitter_tag=twitter_tag,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category='success')

            login_user(user, remember=True)

            return redirect(url_for('views.logged_in_home'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        twitter_tag = request.form.get('twitter_tag')
        password = request.form.get('password')

        user = User.query.filter_by(twitter_tag=twitter_tag).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Succesfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.logged_in_home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('User not found!', category='error')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
