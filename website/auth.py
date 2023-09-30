import tweepy
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

            # update login_user before automatic login. else login_user would be none
            user = User.query.filter_by(twitter_tag=twitter_tag).first()

            flash('Account created!', category='success')

            login_user(user, remember=True)

            return redirect(url_for('views.logged_in_home'))

    return render_template('signup.html', user=current_user)


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

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# twitter authentication


Api_key = "AbGCD0cnJviDRWHD2Eo5tl938"
Api_key_secret = "kpo8bf1CqH9O5gGuUzqzO95Qg4xr7Jn5j9p4WIFvjEhmVPyZIJ"


@auth.route('/twitter_login', methods=['GET', 'POST'])
def twitter_login():
    if request.method == 'POST':
        return redirect(url_for('auth.redirect_to_twitter'))
    else:
        return render_template('twitter_login.html', user=current_user)


@auth.route('/twitter_callback', methods=['GET'])
def twitter_callback():
    # Handle Twitter callback
    oauth_verifier = request.args.get('oauth_verifier')
    oauth1_user_handler = tweepy.OAuth1UserHandler(Api_key, Api_key_secret)
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier)

    print('Success:')
    print(access_token)
    print(access_token_secret)
    # Store the access token and access token secret in your database or session
    # Optionally, you can associate them with the user who just authenticated

    # Redirect to a success page or perform any necessary actions
    return redirect(url_for('auth.success_page'))


@auth.route('/redirect', methods=['GET', 'POST'])
def redirect_to_twitter():
    # 3-legged OAuth - To authenticate as a user other than your developer account
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        Api_key, Api_key_secret,
        # redirecting to this url - after login process finished
        callback='https://www.google.com/'
        # redirect(auth.twitter_callback)
    )
b
    authorisation_URL = oauth1_user_handler.get_authorization_url(
        signin_with_twitter=True)
    return redirect(authorisation_URL)
