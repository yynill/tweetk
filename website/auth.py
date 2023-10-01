import tweepy
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# twitter authentication


Api_key = "AbGCD0cnJviDRWHD2Eo5tl938"
Api_key_secret = "kpo8bf1CqH9O5gGuUzqzO95Qg4xr7Jn5j9p4WIFvjEhmVPyZIJ"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('auth.redirect_to_twitter'))
    else:
        return render_template('login.html', user=current_user)


@auth.route('/twitter_callback', methods=['GET'])
def twitter_callback():
    # Handle Twitter callback
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')

    oauth1_user_handler = tweepy.OAuth1UserHandler(Api_key, Api_key_secret)

    oauth1_user_handler.request_token = {
        "oauth_token": oauth_token,
        "oauth_token_secret": None  # You can set this to the actual secret if available
    }

    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier
    )

   # Store the access token and access token secret in  database
    user = User.query.filter_by(access_token=access_token).first()
    if user:
        flash('Logged in!', category='success')
        login_user(user, remember=True)
    else:
        new_user = User(
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Logged in!', category='success')
        login_user(new_user, remember=True)

    # Redirect to a success page or perform any necessary actions
    return render_template('home_login.html', user=current_user)


@auth.route('/redirect', methods=['GET', 'POST'])
def redirect_to_twitter():
    # 3-legged OAuth - To authenticate as a user other than your developer account
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        Api_key, Api_key_secret,
        # redirecting to this url - after login process finished
        callback='http://127.0.0.1:5000/twitter_callback'
        # redirect(auth.twitter_callback)
        # change when app is live
    )

    authorisation_URL = oauth1_user_handler.get_authorization_url(
        signin_with_twitter=True)
    return redirect(authorisation_URL)
