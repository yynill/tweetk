from flask import Blueprint, render_template
from flask_login import login_required,  current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/home')
@login_required
def logged_in_home():
    return render_template('logged_in_home.html', user=current_user)


@views.route('/pricing')
def pricing():
    return render_template('pricing.html', user=current_user)
