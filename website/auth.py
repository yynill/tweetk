from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        twitter_tag = request.form.get('twitter_tag')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(twitter_tag) == 0:
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
            return redirect(url_for('views.home'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        twitter_tag = request.form.get('twitter_tag')
        password = request.form.get('password')

        user = User.query.filter_by(twitter_tag=twitter_tag).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in SUccesfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('User not found!', category='error')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<h1>logout</h1>"
